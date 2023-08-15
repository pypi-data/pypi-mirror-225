# Copyright 2020 StreamSets Inc.

"""
This module contains project-wide constants.
"""

ENGINE_AUTHENTICATION_METHOD_FORM = 'form'
ENGINE_AUTHENTICATION_METHOD_ASTER = 'aster'

SDC_EXECUTOR_TYPE = 'COLLECTOR'
SNOWFLAKE_EXECUTOR_TYPE = 'SNOWPARK'
SNOWFLAKE_ENGINE_ID = 'SYSTEM_SNOWPARK_ENGINE_ID'
TRANSFORMER_EXECUTOR_TYPE = 'TRANSFORMER'

# This is a dictionary mapping stage names to attribute aliases. As an example, if a particular
# stage had a label updated in a more recent SDC release, the older attribute name should be mapped
# to the newer one.
SDC_STAGE_ATTRIBUTE_RENAME_ALIASES = {
    'com_streamsets_pipeline_stage_destination_couchbase_CouchbaseConnectorDTarget': {
        # https://git.io/fABEc
        'generate_unique_document_key': 'generate_document_key',
        'unique_document_key_field': 'document_key_field',
    },
    'com_streamsets_pipeline_stage_destination_hdfs_HdfsDTarget': {
        # https://git.io/fjCZ1, https://git.io/fjCZD
        'hadoop_fs_configuration': 'additional_configuration',
        'hadoop_fs_configuration_directory': 'configuration_files_directory',
        'hadoop_fs_uri': 'file_system_uri',
        'hdfs_user': 'impersonation_user',
        'validate_hdfs_permissions': 'validate_permissions',
    },
    'com_streamsets_pipeline_stage_destination_s3_AmazonS3DTarget': {
        'bucket': 'bucket_and_path',
    },
    'com_streamsets_pipeline_stage_destination_s3_S3ConnectionTargetConfig': {
        'bucket': 'bucket_and_path',
    },
    'com_streamsets_pipeline_stage_destination_s3_ToErrorAmazonS3DTarget': {
        'bucket': 'bucket_and_path',
    },
    'com_streamsets_pipeline_stage_destination_snowflake_SnowflakeDTarget': {
        # https://git.io/Jednw, https://git.io/JJ61u, https://git.io/JJ61w
        'cdc_data': 'processing_cdc_data',
        'stage_location': 'external_stage_location',
        'external_stage_name': 'snowflake_stage_name',
    },
    'com_streamsets_pipeline_stage_executor_s3_AmazonS3DExecutor': {
        'bucket': 'bucket_and_path',
    },
    'com_streamsets_pipeline_stage_origin_hdfs_HdfsDSource': {
        # https://git.io/fjCZ1, https://git.io/fjCZD
        'hadoop_fs_configuration': 'additional_configuration',
        'hadoop_fs_configuration_directory': 'configuration_files_directory',
        'hadoop_fs_uri': 'file_system_uri',
        'hdfs_user': 'impersonation_user',
    },
    'com_streamsets_pipeline_stage_origin_httpserver_HttpServerDPushSource': {
        # https://git.io/JvBgX
        'application_id': 'list_of_application_ids',
    },
    'com_streamsets_pipeline_stage_origin_jdbc_cdc_oracle_OracleCDCDSource': {
        # https://git.io/Jt6CY
        'use_peg_parser_in_beta': 'use_peg_parser',
    },
    'com_streamsets_pipeline_stage_origin_spooldir_SpoolDirDSource': {
        # https://git.io/vpJ8w
        'max_files_in_directory': 'max_files_soft_limit',
    },
    'com_streamsets_pipeline_stage_origin_startJob_StartJobDSource': {
        # https://git.io/JJsTN
        'delay_between_state_checks': 'status_check_interval',
        'unique_task_name': 'task_name',
        'url_of_control_hub_that_runs_the_specified_jobs': 'control_hub_url',
    },
    'com_streamsets_pipeline_stage_origin_startPipeline_StartPipelineDSource': {
        # https://git.io/JJsTN
        'delay_between_state_checks': 'status_check_interval',
        'control_hub_base_url': 'control_hub_url',
        'unique_task_name': 'task_name',
    },
    'com_streamsets_pipeline_stage_processor_kudulookup_KuduLookupDProcessor': {
        # https://git.io/vpJZF
        'ignore_missing_value': 'ignore_missing_value_in_matching_record',
    },
    'com_streamsets_pipeline_stage_processor_startJob_StartJobDProcessor': {
        # https://git.io/JJsTN
        'delay_between_state_checks': 'status_check_interval',
        'unique_task_name': 'task_name',
        'url_of_control_hub_that_runs_the_specified_jobs': 'control_hub_url',
    },
    'com_streamsets_pipeline_stage_processor_startPipeline_StartPipelineDProcessor': {
        # https://git.io/JJsTN
        'delay_between_state_checks': 'status_check_interval',
        'control_hub_base_url': 'control_hub_url',
        'unique_task_name': 'task_name',
    },
    'com_streamsets_pipeline_stage_processor_waitForJobCompletion_WaitForJobCompletionDProcessor': {
        # https://git.io/JJsTN
        'delay_between_state_checks': 'status_check_interval',
        'url_of_control_hub': 'control_hub_url',
    },
    'com_streamsets_pipeline_stage_processor_waitForPipelineCompletion_WaitForPipelineCompletionDProcessor': {
        # https://git.io/JJsTN
        'delay_between_state_checks': 'status_check_interval',
    },
    'com_streamsets_pipeline_stage_processor_controlHub_ControlHubApiDProcessor': {
        # https://git.io/JOcVh
        'control_hub_api_url': 'control_hub_url',
    },
    'com_streamsets_pipeline_stage_processor_http_HttpDProcessor': {
        'pass_record': 'pass_records',
    },
    'com_streamsets_pipeline_stage_origin_jdbc_cdc_postgres_PostgresCDCDSource': {
        # https://git.io/J1O0w
        'database_time_zone': 'db_time_zone',
    },
}

# This is a dictionary mapping stage names to attribute aliases. As an example, if a particular
# stage had a label updated in a more recent TfS release, the older attribute name should be mapped
# to the newer one.
SNOWFLAKE_STAGE_ATTRIBUTE_RENAME_ALIASES = {

}

# This is a dictionary mapping stage names to attribute aliases. As an example, if a particular
# stage had a label updated in a more recent ST release, the older attribute name should be mapped
# to the newer one.
ST_STAGE_ATTRIBUTE_RENAME_ALIASES = {
    'com_streamsets_pipeline_spark_destination_redshift_RedshiftDDestination': {
        'bucket': 'bucket_and_path',
    },
    'com_streamsets_pipeline_spark_destination_s3_AmazonS3DDestination': {
        'bucket': 'bucket_and_path',
    },
    'com_streamsets_pipeline_spark_origin_jdbc_table_branded_mysql_MySQLJdbcTableDOrigin': {
        'max_number_of_partitions': 'number_of_partitions',
    },
    'com_streamsets_pipeline_spark_origin_jdbc_table_branded_oracle_OracleJdbcTableDOrigin': {
        'max_number_of_partitions': 'number_of_partitions',
    },
    'com_streamsets_pipeline_spark_origin_jdbc_table_branded_postgresql_PostgreJdbcTableDOrigin': {
        'max_number_of_partitions': 'number_of_partitions',
    },
    'com_streamsets_pipeline_spark_origin_jdbc_table_branded_sqlserver_SqlServerJdbcTableDOrigin': {
        'max_number_of_partitions': 'number_of_partitions',
    },
    'com_streamsets_pipeline_spark_origin_redshift_RedshiftDOrigin': {
        'bucket': 'bucket_and_path',
    },
    'com_streamsets_pipeline_spark_origin_s3_AmazonS3DOrigin': {
        'bucket': 'bucket_and_path',
    },
}

# This dictionary maps the stage labels from old labeling to the new ones.
# When calling SDCPipelineBuilder.add_stage('Snowflake SQL Evaluator') it should return the stage with
# label Column Transformer.
SNOWFLAKE_STAGE_RENAME_ALIASES = {
    'Snowflake SQL Evaluator': 'Column Transformer'
}
