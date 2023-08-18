import datetime
import json
import logging
import os
from collections import defaultdict
from types import ModuleType
from typing import Any, Dict, List, Optional, Set, Union

import mlflow
from mlflow.models import Model
from mlflow.utils.file_utils import TempDir, read_yaml
from pyspark.sql import DataFrame
from pyspark.sql.functions import struct

from databricks.feature_store import mlflow_model_constants
from databricks.feature_store._catalog_client_helper import CatalogClientHelper
from databricks.feature_store._spark_client_helper import SparkClientHelper
from databricks.feature_store.catalog_client import CatalogClient
from databricks.feature_store.constants import (
    _WARN,
    MODEL_DATA_PATH_ROOT,
    PREDICTION_COLUMN_NAME,
)
from databricks.feature_store.entities.column_info import ColumnInfo
from databricks.feature_store.entities.data_type import DataType
from databricks.feature_store.entities.feature import Feature
from databricks.feature_store.entities.feature_column_info import FeatureColumnInfo
from databricks.feature_store.entities.feature_function import FeatureFunction
from databricks.feature_store.entities.feature_lookup import FeatureLookup
from databricks.feature_store.entities.feature_spec import FeatureSpec
from databricks.feature_store.entities.feature_table import FeatureTable
from databricks.feature_store.entities.feature_table_info import FeatureTableInfo
from databricks.feature_store.entities.function_info import FunctionInfo
from databricks.feature_store.entities.on_demand_column_info import OnDemandColumnInfo
from databricks.feature_store.entities.source_data_column_info import (
    SourceDataColumnInfo,
)
from databricks.feature_store.information_schema_spark_client import (
    FunctionInfo as UCFunctionInfo,
)
from databricks.feature_store.information_schema_spark_client import (
    InformationSchemaSparkClient,
)
from databricks.feature_store.spark_client import SparkClient
from databricks.feature_store.training_set import TrainingSet, _FseTrainingSet
from databricks.feature_store.utils import (
    request_context,
    schema_utils,
    uc_utils,
    utils,
    utils_common,
    validation_utils,
)
from databricks.feature_store.utils.feature_spec_utils import (
    assign_topological_ordering,
    get_encoded_graph_map,
)
from databricks.feature_store.utils.request_context import RequestContext
from databricks.feature_store.utils.signature_utils import (
    get_mlflow_signature_from_feature_spec,
)
from databricks.feature_store.version import VERSION

_logger = logging.getLogger(__name__)


class TrainingScoringClient:
    def __init__(
        self,
        catalog_client: CatalogClient,
        catalog_client_helper: CatalogClientHelper,
        spark_client: SparkClient,
        spark_client_helper: SparkClientHelper,
        information_schema_spark_client: InformationSchemaSparkClient,
        model_registry_uri: str,
    ):
        self._catalog_client = catalog_client
        self._catalog_client_helper = catalog_client_helper
        self._spark_client = spark_client
        self._spark_client_helper = spark_client_helper
        self._information_schema_spark_client = information_schema_spark_client
        self._model_registry_uri = model_registry_uri

    def create_training_set(
        self,
        df: DataFrame,
        feature_lookups: List[FeatureLookup],
        label: Union[str, List[str], None],
        exclude_columns: List[str],
        **kwargs,
    ) -> TrainingSet:
        req_context = RequestContext(request_context.CREATE_TRAINING_SET)

        # FeatureFunction is allowed as an undocumented type for feature_lookups parameter
        features = feature_lookups
        feature_lookups = [f for f in features if isinstance(f, FeatureLookup)]
        feature_functions = [f for f in features if isinstance(f, FeatureFunction)]

        # Maximum of 100 FeatureFunctions is supported
        if len(feature_functions) > 100:
            raise ValueError("A maximum of 100 FeatureFunctions are supported.")

        # Verify DataFrame type and column uniqueness
        validation_utils.check_dataframe_type(df)
        utils_common.validate_strings_unique(
            df.columns, "Found duplicate DataFrame column names {}."
        )

        # Initialize label_names with empty list if label is not provided
        label_names = utils.as_list(label, [])
        del label

        # Validate label_names, exclude_columns are unique
        utils_common.validate_strings_unique(
            label_names, "Found duplicate label names {}."
        )
        # Verify that label_names is in DataFrame and not in exclude_columns
        for label_name in label_names:
            if label_name not in df.columns:
                raise ValueError(
                    f"Label column '{label_name}' was not found in DataFrame"
                )
            if label_name in exclude_columns:
                raise ValueError(f"Label column '{label_name}' cannot be excluded")

        # Retrieve feature table metadata and Delta table
        table_names = {fl.table_name for fl in feature_lookups}
        feature_table_features_map = self._get_feature_names_for_tables(
            req_context, table_names=table_names
        )
        feature_table_metadata_map = self._get_feature_table_metadata_for_tables(
            req_context, table_names=table_names
        )
        feature_table_data_map = self._load_feature_data_for_tables(
            table_names=table_names
        )

        # Collect SourceDataColumnInfos
        source_data_column_infos = [
            SourceDataColumnInfo(col) for col in df.columns if col not in label_names
        ]
        source_data_names = [sdci.name for sdci in source_data_column_infos]

        # Collect FeatureColumnInfos
        feature_column_infos = self._explode_feature_lookups(
            feature_lookups, feature_table_features_map, feature_table_metadata_map
        )

        # Collect lookback windows
        table_lookback_window_map = self._get_and_validate_lookback_windows(
            feature_lookups
        )

        del feature_lookups

        # Verify features have unique output names
        feature_output_names = [fci.output_name for fci in feature_column_infos]
        utils_common.validate_strings_unique(
            feature_output_names, "Found duplicate feature output names {}."
        )

        # Verify labels do not collide with feature output names
        for label_name in label_names:
            if label_name in feature_output_names:
                raise ValueError(
                    f"Feature cannot have same output name as label '{label_name}'."
                )

        # Verify that FeatureLookup output names do not conflict with source data names
        feature_conflicts = [
            name for name in feature_output_names if name in source_data_names
        ]
        if len(feature_conflicts) > 0:
            feature_conflicts_str = ", ".join(
                [f"'{name}'" for name in feature_conflicts]
            )
            raise ValueError(
                f"DataFrame contains column names that match feature output names specified"
                f" in FeatureLookups: {feature_conflicts_str}. Either remove these columns"
                f" from the DataFrame or FeatureLookups."
            )

        # Validate FeatureLookup data exists (including for columns that will be excluded).
        self._validate_feature_column_infos_data(
            feature_column_infos,
            feature_table_features_map,
            feature_table_data_map,
        )

        # Collect OnDemandColumnInfos
        on_demand_column_infos = [
            OnDemandColumnInfo(
                udf_name=feature_function.udf_name,
                input_bindings=feature_function.input_bindings,
                output_name=feature_function.output_name,
            )
            for feature_function in feature_functions
        ]
        del feature_functions

        on_demand_input_names = utils_common.get_unique_list_order(
            [
                input_name
                for odci in on_demand_column_infos
                for input_name in odci.input_bindings.values()
            ]
        )
        on_demand_output_names = [odci.output_name for odci in on_demand_column_infos]

        # Verify on-demand features have unique output names
        utils_common.validate_strings_unique(
            on_demand_output_names, "Found duplicate on-demand feature output names {}."
        )

        # Verify labels do not collide with on-demand output names
        for label_name in label_names:
            if label_name in on_demand_output_names:
                raise ValueError(
                    f"On-demand feature cannot have same output name as label '{label_name}'."
                )

        # Verify on-demand feature output names do not conflict with source data or feature output names
        source_data_and_feature_output_names = set(
            source_data_names + feature_output_names
        )
        on_demand_conflicts = [
            name
            for name in on_demand_output_names
            if name in source_data_and_feature_output_names
        ]
        if len(on_demand_conflicts) > 0:
            conflicting_on_demand_feature_names = ", ".join(
                f"'{name}'" for name in on_demand_conflicts
            )
            raise ValueError(
                f"FeatureFunctions contains output names that match either DataFrame column names "
                f"or feature output names specified in FeatureLookups: {conflicting_on_demand_feature_names}. "
                f"Either remove these columns from the DataFrame, FeatureLookups, or FeatureFunctions."
            )

        # Validate on-demand and feature inputs exist in either source data or feature or function
        # outputs from previous levels
        all_output_names = source_data_and_feature_output_names.union(
            on_demand_output_names
        )
        missing_on_demand_inputs = set(on_demand_input_names).difference(
            all_output_names
        )
        if len(missing_on_demand_inputs) > 0:
            missing_on_demand_inputs_names = ", ".join(
                [f"'{name}'" for name in sorted(missing_on_demand_inputs)]
            )
            raise ValueError(
                f"Could not find input binding columns {missing_on_demand_inputs_names} required "
                "by FeatureFunctions."
            )

        is_fse_training_set = kwargs.get("is_feature_serving_training_set", False)

        # TODO[ML-34043]: remove this condition once FSE creates complete dummy DF then consolidate
        # this with missing_on_demand_inputs validation.
        if not is_fse_training_set:
            feature_input_names = utils_common.get_unique_list_order(
                [
                    input_name
                    for fci in feature_column_infos
                    for input_name in fci.lookup_key
                ]
            )
            # Validate feature inputs exist in either source data or feature or function outputs
            missing_lookup_inputs = set(feature_input_names).difference(
                all_output_names
            )
            if len(missing_lookup_inputs) > 0:
                missing_input_names = ", ".join(
                    [f"'{name}'" for name in sorted(missing_lookup_inputs)]
                )
                raise ValueError(
                    f"Could not find lookup key columns {missing_input_names} required by "
                    "FeatureLookups."
                )

        uc_function_infos = self._get_uc_function_infos(
            {odci.udf_name for odci in on_demand_column_infos}
        )
        # Validate FeatureFunctions UDFs (including for columns that will be excluded).
        self._validate_on_demand_column_info_udfs(
            on_demand_column_infos=on_demand_column_infos,
            uc_function_infos=uc_function_infos,
        )

        # The order of ColumnInfos in feature_spec.yaml should be:
        # 1. SourceDataColumnInfos: non-label and non-excluded columns from the input DataFrame
        # 2. FeatureColumnInfos: features retrieved through FeatureLookups
        # 3. OnDemandColumnInfos: features created by FeatureFunctions
        column_infos = [
            ColumnInfo(info=info, include=info.output_name not in exclude_columns)
            for info in source_data_column_infos
            + feature_column_infos
            + on_demand_column_infos
        ]
        # Excluded columns that are on-demand inputs or feature lookup keys
        # should still be in feature_spec.yaml with include=False.
        lookup_keys_and_on_demand_inputs = set(on_demand_input_names)
        for fci in feature_column_infos:
            lookup_keys_and_on_demand_inputs.update(fci.lookup_key)

        column_infos = [
            ci
            for ci in column_infos
            if ci.include or ci.output_name in lookup_keys_and_on_demand_inputs
        ]

        # Sort table_infos by table_name, function_infos by udf_name, so they appear sorted in feature_spec.yaml
        # Exclude unnecessary table_infos, function_infos from the FeatureSpec. When a FeatureLookup or FeatureFunction
        # output feature is excluded, the underlying table or UDF is not required in the FeatureSpec.
        consumed_table_names = [
            ci.info.table_name
            for ci in column_infos
            if isinstance(ci.info, FeatureColumnInfo)
        ]
        consumed_table_names = sorted(set(consumed_table_names))
        consumed_udf_names = [
            ci.info.udf_name
            for ci in column_infos
            if isinstance(ci.info, OnDemandColumnInfo)
        ]
        consumed_udf_names = sorted(set(consumed_udf_names))

        table_infos = [
            FeatureTableInfo(
                table_name=table_name,
                table_id=feature_table_metadata_map[table_name].table_id,
                lookback_window=table_lookback_window_map[table_name],
            )
            for table_name in consumed_table_names
        ]
        function_infos = [
            FunctionInfo(udf_name=udf_name) for udf_name in consumed_udf_names
        ]

        # Build FeatureSpec
        feature_spec = FeatureSpec(
            column_infos=assign_topological_ordering(
                column_infos=column_infos,
                # ONLY USED BY FSE. Until ML-33809 is fixed, allow lookup key or function input be
                # missing from source columns.
                allow_missing_source_columns=is_fse_training_set,
            ),
            table_infos=table_infos,
            function_infos=function_infos,
            workspace_id=self._catalog_client.feature_store_workspace_id,
            feature_store_client_version=VERSION,
            serialization_version=FeatureSpec.SERIALIZATION_VERSION_NUMBER,
        )

        # TODO(divyagupta-db): Move validation from _validate_join_feature_data in feature_lookup_utils.py
        #  to a helper function called here and in score_batch.

        # Add consumer of each feature and instrument as final step
        consumer_feature_table_map = defaultdict(list)
        for feature in feature_column_infos:
            consumer_feature_table_map[feature.table_name].append(feature.feature_name)
        additional_add_consumer_headers = {
            request_context.IS_TRAINING_SET_LABEL_SPECIFIED: str(
                bool(label_names)
            ).lower(),
            request_context.NUM_ON_DEMAND_FEATURES_LOGGED: str(
                len(feature_spec.on_demand_column_infos)
            ),
            # Key by consumed_udf_names for determinism, as it is unique and sorted.
            request_context.NUM_LINES_PER_ON_DEMAND_FEATURE: json.dumps(
                [
                    len(uc_function_infos[udf_name].routine_definition.split("\n"))
                    for udf_name in consumed_udf_names
                    # Routine definition will be None if this user is not the owner
                    # of the UDF. This metric will only be instrumented when the
                    # user is the UDF owner.
                    if uc_function_infos[udf_name].routine_definition is not None
                ]
            ),
            # A graph map representing the graph of column infos in the feature spec.
            # Keys are the encoded columns and values are lists of dependencies.
            request_context.FEATURE_SPEC_GRAPH_MAP: json.dumps(
                get_encoded_graph_map(feature_spec.column_infos)
            ),
        }

        add_consumer_req_context = RequestContext.with_additional_custom_headers(
            req_context, additional_add_consumer_headers
        )
        self._catalog_client_helper.add_consumer(
            consumer_feature_table_map, add_consumer_req_context
        )

        if is_fse_training_set:
            return _FseTrainingSet(
                feature_spec,
                df,
                label_names,
                feature_table_metadata_map,
                feature_table_data_map,
                uc_function_infos,
            )
        return TrainingSet(
            feature_spec,
            df,
            label_names,
            feature_table_metadata_map,
            feature_table_data_map,
            uc_function_infos,
        )

    def score_batch(self, model_uri: str, df: DataFrame, result_type: str) -> DataFrame:
        req_context = RequestContext(request_context.SCORE_BATCH)

        validation_utils.check_dataframe_type(df)

        if PREDICTION_COLUMN_NAME in df.columns:
            raise ValueError(
                "FeatureStoreClient.score_batch returns a DataFrame with a new column "
                f'"{PREDICTION_COLUMN_NAME}". df already has a column with name '
                f'"{PREDICTION_COLUMN_NAME}".'
            )

        utils_common.validate_strings_unique(
            df.columns,
            "The provided DataFrame for scoring must have unique column names. Found duplicates {}.",
        )

        # If the user provided an explicit model_registry_uri when constructing the FeatureStoreClient,
        # we respect this by setting the registry URI prior to reading the model from Model
        # Registry.
        if self._model_registry_uri:
            # This command will override any previously set registry_uri.
            mlflow.set_registry_uri(self._model_registry_uri)

        artifact_path = os.path.join(mlflow.pyfunc.DATA, MODEL_DATA_PATH_ROOT)

        with TempDir() as tmp_location:
            local_path = utils.download_model_artifacts(model_uri, tmp_location.path())
            model_data_path = os.path.join(local_path, artifact_path)
            # Augment local workspace metastore tables from 2L to 3L,
            # this will prevent us from erroneously reading data from other catalogs
            feature_spec = uc_utils.get_feature_spec_with_full_table_names(
                FeatureSpec.load(model_data_path)
            )
            raw_model_path = os.path.join(
                model_data_path, mlflow_model_constants.RAW_MODEL_FOLDER
            )
            predict_udf = self._spark_client.get_predict_udf(
                raw_model_path, result_type=result_type
            )
            # TODO (ML-17260) Consider reading the timestamp from the backend instead of feature store artifacts
            ml_model = Model.load(
                os.path.join(local_path, mlflow_model_constants.ML_MODEL)
            )
            model_creation_timestamp_ms = (
                utils.utc_timestamp_ms_from_iso_datetime_string(
                    ml_model.utc_time_created
                )
            )

        # Validate that columns needed for joining feature tables exist and are not duplicates.
        source_column_names = [
            sdci.name for sdci in feature_spec.source_data_column_infos
        ]
        feature_input_keys = []
        for fci in feature_spec.feature_column_infos:
            feature_input_keys.extend([k for k in fci.lookup_key])
        on_demand_input_names = utils_common.get_unique_list_order(
            [
                input_name
                for odci in feature_spec.on_demand_column_infos
                for input_name in odci.input_bindings.values()
            ]
        )
        intermediate_inputs = set(feature_input_keys + on_demand_input_names)

        source_data_names = [
            sdci.name for sdci in feature_spec.source_data_column_infos
        ]
        feature_output_names = [
            fci.output_name for fci in feature_spec.feature_column_infos
        ]
        on_demand_output_names = [
            odci.output_name for odci in feature_spec.on_demand_column_infos
        ]
        all_output_names = set(
            source_data_names + feature_output_names + on_demand_output_names
        )

        required_cols = intermediate_inputs.difference(all_output_names)
        required_cols.update(source_data_names)

        missing_required_columns = [
            col for col in required_cols if col not in df.columns
        ]
        if missing_required_columns:
            missing_columns_formatted = ", ".join(
                [f"'{s}'" for s in missing_required_columns]
            )
            raise ValueError(
                f"DataFrame is missing required columns {missing_columns_formatted}."
            )

        table_names = {fci.table_name for fci in feature_spec.feature_column_infos}
        feature_table_features_map = self._get_feature_names_for_tables(
            req_context, table_names=table_names
        )
        feature_table_metadata_map = self._get_feature_table_metadata_for_tables(
            req_context, table_names=table_names
        )
        feature_table_data_map = self._load_feature_data_for_tables(
            table_names=table_names
        )

        self._validate_feature_column_infos_data(
            feature_spec.feature_column_infos,
            feature_table_features_map,
            feature_table_data_map,
        )

        # Check if the fetched feature tables match the feature tables logged in training
        self._warn_if_tables_mismatched_for_model(
            feature_spec=feature_spec,
            feature_table_metadata_map=feature_table_metadata_map,
            model_creation_timestamp_ms=model_creation_timestamp_ms,
        )

        uc_function_infos = self._get_uc_function_infos(
            {odci.udf_name for odci in feature_spec.on_demand_column_infos}
        )

        # Required source data and feature lookup keys have been validated to exist in `df`.
        # No additional validation is required before resolving FeatureLookups and applying FeatureFunctions.
        augmented_df = TrainingSet(
            feature_spec=feature_spec,
            df=df,
            labels=[],
            feature_table_metadata_map=feature_table_metadata_map,
            feature_table_data_map=feature_table_data_map,
            uc_function_infos=uc_function_infos,
        )._augment_df()

        # Only included FeatureSpec columns should be part of UDF inputs for scoring.
        # Note: extra `df` columns not in FeatureSpec should be preserved.
        udf_input_columns = [
            ci.output_name for ci in feature_spec.column_infos if ci.include
        ]

        # Apply predictions.
        df_with_predictions = augmented_df.withColumn(
            PREDICTION_COLUMN_NAME, predict_udf(struct(*udf_input_columns))
        )

        # Reorder `df_with_predictions` to include:
        # 1. Preserved `df` columns, in `df` column order.
        # 2. Computed model input columns, in `FeatureSpec` column order.
        # 3. Prediction column.
        output_column_order = (
            df.columns
            + [col for col in udf_input_columns if col not in df.columns]
            + [PREDICTION_COLUMN_NAME]
        )
        return_df = df_with_predictions.select(output_column_order)

        # Add consumer of each feature and track the number of overridden features as final step
        consumer_feature_table_map = defaultdict(list)
        for feature in feature_spec.feature_column_infos:
            consumer_feature_table_map[feature.table_name].append(feature.feature_name)

        # Note: Excluded FeatureColumnInfos should not be counted in the number of overridden FeatureLookups.
        materialized_fcis = [
            ci.info
            for ci in feature_spec.column_infos
            if isinstance(ci.info, FeatureColumnInfo) and ci.include
        ]
        overridden_materialized_fcis = [
            fci for fci in materialized_fcis if fci.output_name in df.columns
        ]

        # Compute number of on-demand inputs, and on-demand outputs that are overridden.
        all_fci_output_names = {
            fci.output_name for fci in feature_spec.feature_column_infos
        }
        overridden_odci_inputs = []
        overridden_odcis = []
        for odci in feature_spec.on_demand_column_infos:
            if odci.output_name in df.columns:
                overridden_odcis.append(odci)
            for odci_input in odci.input_bindings.values():
                if odci_input in all_fci_output_names and odci_input in df.columns:
                    overridden_odci_inputs.append(odci_input)

        additional_add_consumer_headers = {
            request_context.NUM_FEATURES_OVERRIDDEN: str(
                len(overridden_materialized_fcis)
            ),
            request_context.NUM_ON_DEMAND_FEATURES_OVERRIDDEN: str(
                len(overridden_odcis)
            ),
            request_context.NUM_ON_DEMAND_FEATURE_INPUTS_OVERRIDDEN: str(
                len(overridden_odci_inputs)
            ),
        }
        add_consumer_req_context = RequestContext.with_additional_custom_headers(
            req_context, additional_add_consumer_headers
        )

        self._catalog_client_helper.add_consumer(
            consumer_feature_table_map, add_consumer_req_context
        )

        return return_df

    def log_model(
        self,
        model: Any,
        artifact_path: str,
        *,
        flavor: ModuleType,
        training_set: Optional[TrainingSet],
        registered_model_name: Optional[str],
        await_registration_for: int,
        **kwargs,
    ):
        # Validate only one of the training_set, feature_spec_path arguments is provided.
        # Retrieve the FeatureSpec, then remove training_set, feature_spec_path from local scope.
        feature_spec_path = kwargs.pop("feature_spec_path", None)
        if (training_set is None) == (feature_spec_path is None):
            raise ValueError(
                "Either 'training_set' or 'feature_spec_path' must be provided, but not both."
            )
        # Retrieve the FeatureSpec and then reformat tables in local metastore to 2L before serialization.
        # This will make sure the format of the feature spec with local metastore tables is always consistent.
        if training_set:
            all_uc_tables = all(
                [
                    uc_utils.is_uc_entity(table_info.table_name)
                    for table_info in training_set.feature_spec.table_infos
                ]
            )
            # training_set.feature_spec is guaranteed to be 3L from FeatureStoreClient.create_training_set.
            feature_spec = uc_utils.get_feature_spec_with_reformat_full_table_names(
                training_set.feature_spec
            )
            label_type_map = training_set._label_data_types
        else:
            # FeatureSpec.load expects the root directory of feature_spec.yaml
            root_dir, file_name = os.path.split(feature_spec_path)
            if file_name != FeatureSpec.FEATURE_ARTIFACT_FILE:
                raise ValueError(
                    f"'feature_spec_path' must be a path to {FeatureSpec.FEATURE_ARTIFACT_FILE}."
                )
            feature_spec = FeatureSpec.load(root_dir)

            # The loaded FeatureSpec is not guaranteed to be 3L.
            # First call get_feature_spec_with_full_table_names to append the default metastore to 2L names,
            # as get_feature_spec_with_reformat_full_table_names expects full 3L table names and throws otherwise.
            # TODO (ML-26593): Consolidate this into a single function that allows either 2L/3L names.
            feature_spec_with_full_table_names = (
                uc_utils.get_feature_spec_with_full_table_names(feature_spec)
            )
            all_uc_tables = all(
                [
                    uc_utils.is_uc_entity(table_info.table_name)
                    for table_info in feature_spec_with_full_table_names.table_infos
                ]
            )
            feature_spec = uc_utils.get_feature_spec_with_reformat_full_table_names(
                feature_spec_with_full_table_names
            )
            # TODO ML-31948: Get output types directly from AutoML as it doesn't pass in training set
            label_type_map = None
        del training_set, feature_spec_path

        override_output_schema = kwargs.pop("output_schema", None)
        with TempDir() as tmp_location:
            data_path = os.path.join(tmp_location.path(), "feature_store")
            raw_mlflow_model = Model()
            raw_model_path = os.path.join(
                data_path, mlflow_model_constants.RAW_MODEL_FOLDER
            )
            if flavor.FLAVOR_NAME != mlflow.pyfunc.FLAVOR_NAME:
                flavor.save_model(
                    model, raw_model_path, mlflow_model=raw_mlflow_model, **kwargs
                )
            else:
                flavor.save_model(
                    raw_model_path,
                    mlflow_model=raw_mlflow_model,
                    python_model=model,
                    **kwargs,
                )
            if not "python_function" in raw_mlflow_model.flavors:
                raise ValueError(
                    f"FeatureStoreClient.log_model does not support '{flavor.__name__}' "
                    f"since it does not have a python_function model flavor."
                )

            # Re-use the conda environment from the raw model for the packaged model. Later, we may
            # add an additional requirement for the Feature Store library. At the moment, however,
            # the databricks-feature-store package is not available via conda or pip.
            model_env = raw_mlflow_model.flavors["python_function"][mlflow.pyfunc.ENV]
            if isinstance(model_env, dict):
                # mlflow 2.0 has multiple supported environments
                conda_file = model_env[mlflow.pyfunc.EnvType.CONDA]
            else:
                conda_file = model_env

            conda_env = read_yaml(raw_model_path, conda_file)

            # Get the pip package string for the databricks-feature-lookup client
            databricks_feature_lookup_pip_package = utils.pip_depependency_pinned_major_version(
                pip_package_name=mlflow_model_constants.FEATURE_LOOKUP_CLIENT_PIP_PACKAGE,
                major_version=mlflow_model_constants.FEATURE_LOOKUP_CLIENT_MAJOR_VERSION,
            )

            # Add pip dependencies required for online feature lookups
            utils.add_mlflow_pip_depependency(
                conda_env, databricks_feature_lookup_pip_package
            )

            # Signatures will ony be supported for UC-table-only models to
            # mitigate new online scoring behavior from being a breaking regression for older
            # models.
            # See https://docs.google.com/document/d/1L5tLY-kRreRefDfuAM3crXvYlirkcPuUUppU8uIMVM0/edit#
            try:
                signature = (
                    get_mlflow_signature_from_feature_spec(
                        feature_spec, label_type_map, override_output_schema
                    )
                    if all_uc_tables
                    else None
                )
            except Exception as e:
                _logger.warning(f"Model could not be logged with a signature: {e}")
                signature = None

            feature_spec.save(data_path)

            # Log the packaged model. If no run is active, this call will create an active run.
            mlflow.pyfunc.log_model(
                artifact_path=artifact_path,
                loader_module=mlflow_model_constants.MLFLOW_MODEL_NAME,
                data_path=data_path,
                code_path=None,
                conda_env=conda_env,
                signature=signature,
            )
        if registered_model_name is not None:
            # The call to mlflow.pyfunc.log_model will create an active run, so it is safe to
            # obtain the run_id for the active run.
            run_id = mlflow.tracking.fluent.active_run().info.run_id

            # If the user provided an explicit model_registry_uri when constructing the FeatureStoreClient,
            # we respect this by setting the registry URI prior to reading the model from Model
            # Registry.
            if self._model_registry_uri:
                # This command will override any previously set registry_uri.
                mlflow.set_registry_uri(self._model_registry_uri)

            mlflow.register_model(
                "runs:/%s/%s" % (run_id, artifact_path),
                registered_model_name,
                await_registration_for=await_registration_for,
            )

    def _get_uc_function_infos(self, udf_names: Set[str]) -> Dict[str, UCFunctionInfo]:
        # Note: Only GetFunction ACLs are required here. ExecuteFunction ACL will be checked at SQL execution.
        function_infos = self._information_schema_spark_client.get_functions(
            list(udf_names)
        )
        return {
            function_info.full_name: function_info for function_info in function_infos
        }

    def _get_feature_names_for_tables(
        self, req_context: RequestContext, table_names: Set[str]
    ) -> Dict[str, List[Feature]]:
        """
        Lookup features from the feature catalog for all table_names, return a dictionary of tablename -> list of features.
        """
        return {
            table_name: self._catalog_client.get_features(table_name, req_context)
            for table_name in table_names
        }

    def _get_feature_table_metadata_for_tables(
        self, req_context: RequestContext, table_names: Set[str]
    ) -> Dict[str, FeatureTable]:
        """
        Lookup FeatureTable metadata from the feature catalog for all table_names, return a dictionary of tablename -> FeatureTable.
        """
        return {
            table_name: self._catalog_client.get_feature_table(table_name, req_context)
            for table_name in table_names
        }

    def _load_feature_data_for_tables(
        self, table_names: Set[str]
    ) -> Dict[str, DataFrame]:
        """
        Load feature DataFrame objects for all table_names, return a dictionary of tablename -> DataFrame.
        """
        return {
            table_name: self._spark_client.read_table(table_name)
            for table_name in table_names
        }

    def _explode_feature_lookups(
        self,
        feature_lookups: List[FeatureLookup],
        feature_table_features_map: Dict[str, List[Feature]],
        feature_table_metadata_map: Dict[str, FeatureTable],
    ) -> List[FeatureColumnInfo]:
        """
        Explode FeatureLookups and collect into FeatureColumnInfos. A FeatureLookup may explode into either:
        1. A single FeatureColumnInfo, in the case where only a single feature name is specified.
        2. Multiple FeatureColumnInfos, in the cases where either multiple or all feature names are specified.

        When all features are specified in a FeatureLookup (feature_names is None),
        FeatureColumnInfos will be created for all features except primary and timestamp keys.
        The order of FeatureColumnInfos returned will be the same as the order returned by GetFeatures:
        1. All partition keys that are not primary keys, in the partition key order.
        2. All other non-key features in alphabetical order.
        """
        feature_column_infos = []
        for feature_lookup in feature_lookups:
            feature_column_infos_for_feature_lookup = self._explode_feature_lookup(
                feature_lookup=feature_lookup,
                features=feature_table_features_map[feature_lookup.table_name],
                feature_table=feature_table_metadata_map[feature_lookup.table_name],
            )
            feature_column_infos += feature_column_infos_for_feature_lookup
        return feature_column_infos

    def _explode_feature_lookup(
        self,
        feature_lookup: FeatureLookup,
        features: List[Feature],
        feature_table: FeatureTable,
    ) -> List[FeatureColumnInfo]:
        feature_names = []
        if feature_lookup._get_feature_names():
            # If the user explicitly passed in a feature name or list of feature names, use that
            feature_names.extend(feature_lookup._get_feature_names())
        else:
            # Otherwise assume the user wants all columns in the feature table
            keys = {*feature_table.primary_keys, *feature_table.timestamp_keys}
            feature_names.extend(
                [feature.name for feature in features if feature.name not in keys]
            )

        return [
            FeatureColumnInfo(
                table_name=feature_lookup.table_name,
                feature_name=feature_name,
                lookup_key=utils.as_list(feature_lookup.lookup_key),
                output_name=(feature_lookup._get_output_name(feature_name)),
                timestamp_lookup_key=utils.as_list(
                    feature_lookup.timestamp_lookup_key, default=[]
                ),
            )
            for feature_name in feature_names
        ]

    def _warn_if_tables_mismatched_for_model(
        self,
        feature_spec: FeatureSpec,
        feature_table_metadata_map: Dict[str, FeatureTable],
        model_creation_timestamp_ms: float,
    ):
        """
        Helper method to warn if feature tables were deleted and recreated after a model was logged.
        For newer FeatureSpec versions >=3, we can compare the FeatureSpec and current table ids.
        Otherwise, we compare the model and table creation timestamps.
        """
        # 1. Compare feature table ids
        # Check for feature_spec logged with client versions that supports table_infos
        if len(feature_spec.table_infos) > 0:
            # When feature_spec.yaml is parsed, FeatureSpec.load will assert
            # that the listed table names in input_tables match table names in input_columns.
            # The following code assumes this as invariant and only checks for the table IDs.
            mismatched_tables = []
            for table_info in feature_spec.table_infos:
                feature_table = feature_table_metadata_map[table_info.table_name]
                if feature_table and table_info.table_id != feature_table.table_id:
                    mismatched_tables.append(table_info.table_name)
            if len(mismatched_tables) > 0:
                plural = len(mismatched_tables) > 1
                _logger.warning(
                    f"Feature table{'s' if plural else ''} {', '.join(mismatched_tables)} "
                    f"{'were' if plural else 'was'} deleted and recreated after "
                    f"the model was trained. Model performance may be affected if the features "
                    f"used in scoring have drifted from the features used in training."
                )

        # 2. Compare model creation timestamp with feature table creation timestamps
        feature_tables_created_after_model = []
        for name, metadata in feature_table_metadata_map.items():
            if model_creation_timestamp_ms < metadata.creation_timestamp:
                feature_tables_created_after_model.append(name)
        if len(feature_tables_created_after_model) > 0:
            plural = len(feature_tables_created_after_model) > 1
            message = (
                f"Feature table{'s' if plural else ''} {', '.join(feature_tables_created_after_model)} "
                f"{'were' if plural else 'was'} created after the model was logged. "
                f"Model performance may be affected if the features used in scoring have drifted "
                f"from the features used in training."
            )
            _logger.warning(message)

    def _validate_feature_column_infos_data(
        self,
        feature_column_infos: List[FeatureColumnInfo],
        features_by_table: Dict[str, List[Feature]],
        feature_table_data_map: Dict[str, DataFrame],
    ):
        """
        Validates required FeatureLookup data. Checks:
        1. Feature tables exist in Delta.
        2. Feature data types match in Delta and Feature Catalog.
        """
        table_to_features = defaultdict(list)
        for fci in feature_column_infos:
            table_to_features[fci.table_name].append(fci.feature_name)

        for table_name, features_in_spec in table_to_features.items():
            self._spark_client_helper.check_feature_table_exists(table_name)

            catalog_features = features_by_table[table_name]
            feature_table_data = feature_table_data_map[table_name]
            catalog_schema = {
                feature.name: feature.data_type for feature in catalog_features
            }
            delta_schema = {
                feature.name: DataType.spark_type_to_string(feature.dataType)
                for feature in feature_table_data.schema
            }

            for feature_name in features_in_spec:
                if feature_name not in catalog_schema:
                    raise ValueError(
                        f"Unable to find feature '{feature_name}' from feature table '{table_name}' in Feature Catalog."
                    )
                if feature_name not in delta_schema:
                    raise ValueError(
                        f"Unable to find feature '{feature_name}' from feature table '{table_name}' in Delta."
                    )
                if catalog_schema[feature_name] != delta_schema[feature_name]:
                    raise ValueError(
                        f"Expected type of feature '{feature_name}' from feature table '{table_name}' "
                        f"to be equivalent in Feature Catalog and Delta. "
                        f"Feature has type '{catalog_schema[feature_name]}' in Feature Catalog and "
                        f"'{delta_schema[feature_name]}' in Delta."
                    )

            # Warn if mismatch in other features in feature table
            if not schema_utils.catalog_matches_delta_schema(
                catalog_features, feature_table_data.schema
            ):
                schema_utils.log_catalog_schema_not_match_delta_schema(
                    catalog_features,
                    feature_table_data.schema,
                    level=_WARN,
                )

    def _get_and_validate_lookback_windows(
        self,
        feature_lookups: List[FeatureLookup],
    ) -> Dict[str, Optional[datetime.timedelta]]:
        """
        Gets lookback_window values from all feature_lookups, validates that lookback_window values are consistent per feature table,
        and returns a dictionary of tablename -> lookback_window values. In the case where lookback_window is not defined, the key value
        mapping will be "feature_table_name" -> None.
        """
        table_lookback_windows_map = defaultdict(set)
        for fl in feature_lookups:
            table_lookback_windows_map[fl.table_name].add(fl.lookback_window)

        for table_name, lookback_windows in table_lookback_windows_map.items():
            if len(set(lookback_windows)) > 1:
                if None in lookback_windows:
                    raise ValueError(
                        f"lookback_window values must be consistently defined per feature table. '{table_name}' has "
                        f"missing lookback_window values: {lookback_windows}."
                    )
                else:
                    raise ValueError(
                        f"Only one value for lookback_window can be defined per feature table. '{table_name}' has "
                        f"conflicting lookback_window values: {lookback_windows}."
                    )
        return {
            k: next(iter(v)) for k, v in table_lookback_windows_map.items()
        }  # Get the only element from a single member set

    def _validate_on_demand_column_info_udfs(
        self,
        on_demand_column_infos: List[OnDemandColumnInfo],
        uc_function_infos: Dict[str, UCFunctionInfo],
    ):
        """
        Validates OnDemandColumnInfo UDFs can be applied as on-demand features. Checks:
        1. UDF is defined in Python.
        2. UDF input parameters are consistent with its input bindings.

        Note: Provided UC FunctionInfos not required by OnDemandColumnInfos are not validated.
        """
        for odci in on_demand_column_infos:
            function_info = uc_function_infos[odci.udf_name]
            if function_info.external_language != UCFunctionInfo.PYTHON:
                raise ValueError(
                    f"FeatureFunction UDF '{odci.udf_name}' is not a Python UDF. Only Python UDFs are supported."
                )

            udf_input_params = [p.name for p in function_info.input_params]
            if odci.input_bindings.keys() != set(udf_input_params):
                raise ValueError(
                    f"FeatureFunction UDF '{odci.udf_name}' input parameters {udf_input_params} "
                    f"do not match input bindings {odci.input_bindings}."
                )
