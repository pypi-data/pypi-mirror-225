# create logger
import json
from pathlib import Path
from typing import Optional, List, Tuple

import typer
from bigeye_sdk.client.enum import Method

from bigeye_cli.enums import OPS_METRICS
from bigeye_cli import global_options
from bigeye_sdk.model.protobuf_enum_facade import MetricStatus, SimpleMetricCategory, SimpleMetricTemplateParameterType, \
    SimpleMetricTemplateFieldType
from bigeye_sdk.functions.aws import get_secret
from bigeye_sdk.generated.com.bigeye.models.generated import MetricInfoList, WarehouseType, CreateSourceRequest, \
    TimeIntervalType, PredefinedMetricName, MetricCreationState, MetricConfiguration, ForecastModelType, Source, Table
from bigeye_sdk.log import get_logger
from bigeye_cli.functions import write_metric_info, cli_client_factory, write_table_info, write_debug_queries, \
    write_metric_templates
from bigeye_sdk.functions.metric_functions import has_auto_threshold
from bigeye_sdk.functions.core_py_functs import int_enum_enum_list_joined

log = get_logger(__file__)

app = typer.Typer(no_args_is_help=True, help='Catalog Commands for Bigeye CLI')

"""
File should contain commands that will impact catalog, table, or schema level changes to a Bigeye workspace.  This
would include metrics batched at any of these levels.
"""


@app.command()
def regen_autometrics(
        bigeye_conf: str = global_options.bigeye_conf,
        config_file: str = global_options.config_file,
        workspace: str = global_options.workspace,
        warehouse_id: int = typer.Option(
            None
            , "--warehouse_id"
            , "-wid"
            , help="Warehouse ID.  If none will look for Table IDs.  If value then will pull all table ids for "
                   "warehouse"),
        schema_names: Optional[List[str]] = typer.Option(
            None
            , "--schema_name"
            , "-sn"
            , help="List of Schema Names  E.g. -sn schema_1 -sn schema_2.  Do not include warehouse name -- "
                   "GREENE_HOMES_DEMO_STANDARD.CONFORMED is fully qualified and CONFORMED is the schema name."),
        table_ids: Optional[List[int]] = typer.Option(
            None
            , "--table_id"
            , "-tid"
            , help="List of Table IDs.  E.g. -tid 123 -tid 124")
):
    """Regenerates Autometrics by warehouse id OR warehouse id and list of schema names OR list of table ids."""
    client = cli_client_factory(bigeye_conf, config_file, workspace)

    if not table_ids:
        table_ids = client.get_table_ids(warehouse_id=[warehouse_id], schemas=schema_names)

    if table_ids:
        log.info(f'Regenerating autometrics on: {table_ids}')
        for tid in table_ids:
            client.regen_autometrics(table_id=tid)
    else:
        raise Exception('Could not identify table_ids to run.  Provide either a valid list of table ids OR a valid '
                        'warehouse ID OR a valid warehouse ID and list of valid schema names')


@app.command()
def deploy_all_autometrics(
        bigeye_conf: str = global_options.bigeye_conf,
        config_file: str = global_options.config_file,
        workspace: str = global_options.workspace,
        warehouse_id: int = typer.Option(
            None
            , "--warehouse_id"
            , "-wid"
            , help="Deploy autometrics to all tables in warehouse."),
        schema_names: Optional[List[str]] = typer.Option(
            None
            , "--schema_name"
            , "-sn"
            , help="List of Schema Names.  E.g. -sn schema_1 -sn schema_2."),
        table_ids: Optional[List[int]] = typer.Option(
            None
            , "--table_id"
            , "-tid"
            , help="Table IDs.  E.g. -tid 123 -tid 124"),
        lookback_days: int = typer.Option(
            7
            , "--lookback_days"
            , "-lbd"
            , help="Look back days for the metrics."
        ),
        ops_only: bool = typer.Option(
            True
            , "--ops_only"
            , help="Deploy only operational metrics")
):
    """Deploys all Autometrics to specified warehouse OR warehouse and list of schema names OR warehouse and list of
    table ids."""
    # TODO: Add operational metrics only code.
    log.info(f'Deploying all metrics.')
    log.info(f'Bigeye API Configuration: {bigeye_conf} | Warehouse ID: {warehouse_id} | Table IDs: {table_ids}')

    client = cli_client_factory(bigeye_conf, config_file, workspace)

    ms = MetricCreationState.METRIC_CREATION_STATE_SUGGESTED_AUTO

    mil = MetricInfoList()

    if not schema_names:
        mil = client.get_metric_info_batch_post(warehouse_ids=[warehouse_id], table_ids=table_ids,
                                                metric_creation_states=[ms])

    if schema_names:
        for sn in schema_names:
            submil = client.get_metric_info_batch_post(warehouse_ids=[warehouse_id], table_ids=table_ids,
                                                       metric_creation_states=[ms], schema_name=sn)
            mil.metrics.extend(submil.metrics)

    if ops_only:
        mil.metrics = [m for m in mil.metrics if m.metric_configuration.metric_type.predefined_metric in OPS_METRICS]

    mids: List[int] = [m.metric_configuration.id for m in mil.metrics]

    client.accept_autometrics(metric_ids=mids, lookback_days=lookback_days)


@app.command()
def delete_metrics(
        bigeye_conf: str = global_options.bigeye_conf,
        config_file: str = global_options.config_file,
        workspace: str = global_options.workspace,
        warehouse_id: int = typer.Option(
            None
            , "--warehouse_id"
            , "-wid"
            , help="Warehouse ID"),
        schema_names: Optional[List[str]] = typer.Option(
            None
            , "--schema_name"
            , "-sn"
            , help="List of Schema Names.  E.g. -sn schema_1 -sn schema_2."),

        table_ids: Optional[List[int]] = typer.Option(
            None
            , "--table_id"
            , "-tid"
            , help="Table IDs.  E.g. -tid 123 -tid 124"),
        metric_type: Optional[List[str]] = typer.Option(
            None
            , "--metric_type"
            , "-m"
            , help=f"Delete by name of the metric type."
                   f"{', '.join([i.name for i in PredefinedMetricName])}"),
):
    """Delete metrics in a warehouse id, by schema names, or by table_ids.  Also, can filter by multipe
    metric types."""
    client = cli_client_factory(bigeye_conf, config_file, workspace)

    mil: MetricInfoList = client.get_metric_info_batch_post(warehouse_ids=[warehouse_id],
                                                            table_ids=table_ids)

    if schema_names:
        mil.metrics = [m for m in mil.metrics if m.metric_metadata.schema_name in schema_names]

    if metric_type:
        mil.metrics = [m for m in mil.metrics
                       if SimpleMetricCategory.get_metric_name(m.metric_configuration.metric_type) in metric_type]

    metrics = [m.metric_configuration for m in mil.metrics]

    client.delete_metrics(metrics=metrics)


@app.command()
def rebuild(
        bigeye_conf: str = global_options.bigeye_conf,
        config_file: str = global_options.config_file,
        workspace: str = global_options.workspace,
        warehouse_id: int = typer.Option(
            ...
            , "--warehouse_id"
            , "-wid"
            , help="Warehouse ID"),
        schema_name: str = typer.Option(
            None
            , "--schema_name"
            , "-sn"
            , help="Schema Name"),
):
    """Rebuilds/Reprofiles a source by warehouse id or a schema by warehouse id and schema name."""
    client = cli_client_factory(bigeye_conf, config_file, workspace)

    log.info(f'Rebuilding Catalog Resource.  Warehouse ID: {warehouse_id}  Schema Name: {schema_name}')
    client.rebuild(warehouse_id=warehouse_id, schema_name=schema_name)


@app.command()
def get_table_info(
        bigeye_conf: str = global_options.bigeye_conf,
        config_file: str = global_options.config_file,
        workspace: str = global_options.workspace,
        warehouse_id: int = typer.Option(
            None
            , "--warehouse_id"
            , "-wid"
            , help="Warehouse ID"),
        schema_names: Optional[List[str]] = typer.Option(
            None
            , "--schema_name"
            , "-sn"
            , help="List of Schema Names.  E.g. -sn schema_1 -sn schema_2."),

        table_ids: Optional[List[int]] = typer.Option(
            None
            , "--table_id"
            , "-tid"
            , help="Table IDs. E.g. -tid 123 -tid 124"),
        table_names: Optional[List[str]] = typer.Option(
            None
            , "--table_name"
            , "-tn"
            , help="Table Namess. E.g. -tn some_table -tn some_other_table"),
        output_path: str = typer.Option(
            ...
            , "--output_path"
            , "-op"
            , help="File to write the failed metric configurations to.")
):
    """Outputs table info to a file for an entire warehouse, certain schemas, or certain tables."""
    client = cli_client_factory(bigeye_conf, config_file, workspace)

    wids = [] if not warehouse_id else [warehouse_id]

    tables = client.get_tables(warehouse_id=wids, schema=schema_names,
                               ids=table_ids, table_name=table_names)

    write_table_info(output_path=output_path, tables=tables.tables)


@app.command()
def get_metric_info(
        bigeye_conf: str = global_options.bigeye_conf,
        config_file: str = global_options.config_file,
        workspace: str = global_options.workspace,
        warehouse_id: int = typer.Option(
            None
            , "--warehouse_id"
            , "-wid"
            , help="Warehouse ID"),
        schema_names: Optional[List[str]] = typer.Option(
            None
            , "--schema_name"
            , "-sn"
            , help="List of Schema Names.  E.g. -sn schema_1 -sn schema_2."),

        table_ids: Optional[List[int]] = typer.Option(
            None
            , "--table_id"
            , "-tid"
            , help="Table IDs. E.g. -tid 123 -tid 124"
                   "or schema names."),
        metric_status: MetricStatus = typer.Option(
            None
            , "--metric_status"
            , "-ms"
            , help="Used to query metric of particular status."),
        output_path: str = typer.Option(
            ...
            , "--output_path"
            , "-op"
            , help="File to write the failed metric configurations to."),
        only_metric_conf: bool = typer.Option(
            False
            , "--conf_only"
            , help="Output only the metric configuration.")
):
    """Outputs metric info to a file.  Includes metric configuration and details about recent runs."""
    client = cli_client_factory(bigeye_conf, config_file, workspace)

    if metric_status:
        metric_status_name = metric_status.name
    else:
        metric_status_name = None

    mil: MetricInfoList = client.get_metric_info_batch_post(warehouse_ids=[warehouse_id],
                                                            table_ids=table_ids,
                                                            status=metric_status_name)

    if schema_names:
        mil.metrics = [m for m in mil.metrics if m.metric_metadata.schema_name in schema_names]

    write_metric_info(output_path=output_path, metrics=mil, only_metric_conf=only_metric_conf)


@app.command()
def run_metrics(
        bigeye_conf: str = global_options.bigeye_conf,
        config_file: str = global_options.config_file,
        workspace: str = global_options.workspace,
        warehouse_id: int = typer.Option(
            None
            , "--warehouse_id"
            , "-wid"
            , help="Warehouse ID"),
        schema_names: Optional[List[str]] = typer.Option(
            None
            , "--schema_name"
            , "-sn"
            , help="List of Schema Names.  E.g. -sn schema_1 -sn schema_2."),

        table_ids: Optional[List[int]] = typer.Option(
            None
            , "--table_id"
            , "-tid"
            , help="Table IDs. E.g. -tid 123 -tid 124"),
        table_names: Optional[List[str]] = typer.Option(
            None
            , "--table_name"
            , "-tn"
            , help="Table Names. E.g. -tn some_table -tn some_other_table")
):
    """Runs all metrics for a warehouse, particular schemas in a warehouse, or tables by id."""
    client = cli_client_factory(bigeye_conf, config_file, workspace)

    wids = [] if not warehouse_id else [warehouse_id]

    mil = client.get_metric_info_batch_post(warehouse_ids=wids, table_ids=table_ids)

    if schema_names and table_names:
        mids = [m.metric_configuration.id for m in mil.metrics
                if m.metric_metadata.schema_name in schema_names and m.metric_metadata.dataset_name in table_names]
    elif schema_names:
        mids = [m.metric_configuration.id for m in mil.metrics if m.metric_metadata.schema_name in schema_names]
    elif table_names:
        mids = [m.metric_configuration.id for m in mil.metrics if m.metric_metadata.dataset_name in table_names]
    else:
        mids = [m.metric_configuration.id for m in mil.metrics]

    r = client.run_metric_batch(metric_ids=mids)
    log.info(r.to_json())


@app.command()
def add_source(
        bigeye_conf: str = global_options.bigeye_conf,
        config_file: str = global_options.config_file,
        workspace: str = global_options.workspace,
        secret_name: str = typer.Option(
            None
            , "--secret_name"
            , "-sn"
            , help="""The name of the secret to retrieve from AWS Secrets Manager"""),
        secret_region_name: str = typer.Option(
            'us-west-2'
            , "--secret_region_name"
            , "-srn"
            , help="AWS Secret Manager Region Name"),
        source_catalog_config_file: str = typer.Option(
            None
            , "--source_catalog_config_file"
            , "-sccf"
            , help="The file containing the necessary parameters for adding a source to Bigeye."
        )
):
    """Adds a source to specified Bigeye workspace.  Supports either source configs stored in AWS Secrets manager OR
    locally in file."""
    client = cli_client_factory(bigeye_conf, config_file, workspace)

    if secret_name:
        secret = get_secret(secret_name, secret_region_name)
        source_config = json.loads(secret['SecretString'])
    else:
        log.info(f'Loading source config file: {source_catalog_config_file}')
        with open(source_catalog_config_file) as json_file:
            source_config = json.load(json_file)

    db_type = source_config['database_type'].upper()
    source_config['database_type'] = WarehouseType[f'DATABASE_TYPE_{db_type}']

    client.create_source(CreateSourceRequest(**source_config))


@app.command()
def delete_source(
        bigeye_conf: str = global_options.bigeye_conf,
        config_file: str = global_options.config_file,
        workspace: str = global_options.workspace,
        warehouse_id: int = typer.Option(
            None
            , "--warehouse_id"
            , "-wid"
            , help="""The ID of the warehouse to delete."""),
):
    """Delete a source from specified Bigeye workspace."""
    client = cli_client_factory(bigeye_conf, config_file, workspace)

    client.delete_source(warehouse_id)


@app.command()
def backfill_autothresholds(
        bigeye_conf: str = global_options.bigeye_conf,
        config_file: str = global_options.config_file,
        workspace: str = global_options.workspace,
        warehouse_id: int = typer.Option(
            None
            , "--warehouse_id"
            , "-wid"
            , help="Warehouse ID"),
        schema_names: Optional[List[str]] = typer.Option(
            None
            , "--schema_name"
            , "-sn"
            , help="List of Schema Names.  E.g. -sn schema_1 -sn schema_2."),

        table_ids: Optional[List[int]] = typer.Option(
            None
            , "--table_id"
            , "-tid"
            , help="Table IDs.  E.g. -tid 123 -tid 124")
):
    """Backfills autothresholds by warehouse id, schema names, and/or table ids."""
    client = cli_client_factory(bigeye_conf, config_file, workspace)

    mil: MetricInfoList = client.get_metric_info_batch_post(warehouse_ids=[warehouse_id],
                                                            table_ids=table_ids)
    if schema_names:
        mil.metrics = [m for m in mil.metrics if m.metric_metadata.schema_name in schema_names]

    mids = [m.metric_configuration.id for m in mil.metrics if has_auto_threshold(m.metric_configuration.thresholds)]

    client.backfill_autothresholds(metric_ids=mids)


@app.command()
def backfill_metrics(
        bigeye_conf: str = global_options.bigeye_conf,
        config_file: str = global_options.config_file,
        workspace: str = global_options.workspace,
        warehouse_id: int = typer.Option(
            None
            , "--warehouse_id"
            , "-wid"
            , help="Warehouse ID"),
        schema_names: Optional[List[str]] = typer.Option(
            None
            , "--schema_name"
            , "-sn"
            , help="List of Schema Names.  E.g. -sn schema_1 -sn schema_2."),

        table_ids: Optional[List[int]] = typer.Option(
            None
            , "--table_id"
            , "-tid"
            , help="Table IDs.  E.g. -tid 123 -tid 124"),

        delete_history: Optional[bool] = typer.Option(
            None
            , "--delete_history"
            , help="Delete metric run history"
        )
):
    """Backfills metrics by warehouse id, schema names, and/or table ids."""
    client = cli_client_factory(bigeye_conf, config_file, workspace)

    mil: MetricInfoList = client.get_metric_info_batch_post(warehouse_ids=[warehouse_id],
                                                            table_ids=table_ids)
    if schema_names:
        mil.metrics = [m for m in mil.metrics if m.metric_metadata.schema_name in schema_names]

    metadata_metric_mids = [m.metric_configuration.id for m in mil.metrics if m.metric_configuration.metric_type]

    mids = [m.metric_configuration.id for m in mil.metrics]

    for mid in mids:
        try:
            client.backfill_metric(metric_ids=[mid], delete_history=delete_history)
        except Exception as e:
            log.exception(e)
    client.run_metric_batch(metric_ids=mids)


@app.command()
def run_metrics(
        bigeye_conf: str = global_options.bigeye_conf,
        config_file: str = global_options.config_file,
        workspace: str = global_options.workspace,
        warehouse_id: int = typer.Option(
            None
            , "--warehouse_id"
            , "-wid"
            , help="Warehouse ID"),
        schema_names: Optional[List[str]] = typer.Option(
            None
            , "--schema_name"
            , "-sn"
            , help="List of Schema Names.  E.g. -sn schema_1 -sn schema_2."),

        table_ids: Optional[List[int]] = typer.Option(
            None
            , "--table_id"
            , "-tid"
            , help="Table IDs.  E.g. -tid 123 -tid 124")
):
    """Runs metrics by warehouse id, schema names, and/or table ids"""
    client = cli_client_factory(bigeye_conf, config_file, workspace)

    mil: MetricInfoList = client.get_metric_info_batch_post(warehouse_ids=[warehouse_id],
                                                            table_ids=table_ids)
    if schema_names:
        mil.metrics = [m for m in mil.metrics if m.metric_metadata.schema_name in schema_names]

    metadata_metric_mids = [m.metric_configuration.id for m in mil.metrics if m.metric_configuration.metric_type]

    mids = [m.metric_configuration.id for m in mil.metrics]

    client.run_metric_batch(metric_ids=mids)


@app.command()
def schedule_all_metrics(
        bigeye_conf: str = global_options.bigeye_conf,
        config_file: str = global_options.config_file,
        workspace: str = global_options.workspace,
        warehouse_id: int = typer.Option(
            None
            , "--warehouse_id"
            , "-wid"
            , help="Warehouse ID"),
        time_interval_type: int = typer.Option(
            TimeIntervalType.HOURS_TIME_INTERVAL_TYPE.value
            , "--time_interval_type"
            , "-type"
            , help=f"Time interval type.\n {int_enum_enum_list_joined(enum=TimeIntervalType)}"),
        interval_value: int = typer.Option(
            ...
            , "--interval_value"
            , "-value"
            , help="Number of intervals to set on all metric schedules.  If 0 use unschedule all metrics.")
):
    """Updates schedule for all metrics in a warehouse."""
    client = cli_client_factory(bigeye_conf, config_file, workspace)

    tit = TimeIntervalType(time_interval_type)

    wids: List[int] = [warehouse_id]

    # Could do bulk change by wid and metric type which are necessary in the api call.
    mcs: List[MetricConfiguration] = [mil.metric_configuration
                                      for mil in client.get_metric_info_batch_post(warehouse_ids=wids).metrics]

    for mc in mcs:
        body = mc.to_dict()
        body['scheduleFrequency']['intervalType'] = tit.name
        body['scheduleFrequency']['intervalValue'] = interval_value
        if 'thresholds' in body:
            body.pop('thresholds')

        url = "/api/v1/metrics"

        response = client._call_datawatch(Method.POST, url=url, body=json.dumps(body))


@app.command()
def unschedule_all_metrics(
        bigeye_conf: str = global_options.bigeye_conf,
        config_file: str = global_options.config_file,
        workspace: str = global_options.workspace,
        warehouse_id: int = typer.Option(
            None
            , "--warehouse_id"
            , "-wid"
            , help="Warehouse ID"),
        schema_name: Optional[str] = typer.Option(
            None
            , "--schema_name"
            , "-sn"
            , help="List of Schema Name.  E.g. -sn schema_1."),

        table_ids: Optional[List[int]] = typer.Option(
            None
            , "--table_id"
            , "-tid"
            , help="Table IDs.  E.g. -tid 123 -tid 124")
):
    """Unschedule all metrics by warehouse, schema or tables."""
    client = cli_client_factory(bigeye_conf, config_file, workspace)

    mcs: List[MetricConfiguration] = [mil.metric_configuration
                                      for mil in client.get_metric_info_batch_post(warehouse_ids=[warehouse_id],
                                                                                   schema_name=schema_name,
                                                                                   table_ids=table_ids).metrics]
    url = '/api/v1/metrics'

    for mc in mcs:
        body = mc.to_dict()
        body["scheduleFrequency"] = {
            "intervalType": TimeIntervalType.MINUTES_TIME_INTERVAL_TYPE,
            "intervalValue": 0
        }
        if 'thresholds' in body:
            for t in body["thresholds"]:
                if 'autoThreshold' in t:
                    t["autoThreshold"]["modelType"] = ForecastModelType.BOOTSTRAP_THRESHOLD_MODEL_TYPE

        response = client._call_datawatch(Method.POST, url=url, body=json.dumps(body))


@app.command()
def set_metric_time(
        bigeye_conf: str = global_options.bigeye_conf,
        config_file: str = global_options.config_file,
        workspace: str = global_options.workspace,
        warehouse_id: int = typer.Option(
            None
            , "--warehouse_id"
            , "-wid"
            , help="Warehouse ID"),
        schema_id: Optional[int] = typer.Option(
            None
            , "--schema_id"
            , "-sid"
            , help="Schema ID"),
        table_ids: Optional[List[int]] = typer.Option(
            None
            , "--table_id"
            , "-tid"
            , help="List of table IDs."),
        metric_column_names: Optional[List[str]] = typer.Option(
            ...
            , "--metric_column_name"
            , "-cn"
            , help="Possible metric column names."),
        replace_set_metric_times: bool = typer.Option(
            False
            , "--replace"
            , "-r"
            , help="replace metric times if already present on tables?  Default is false."
        )
):
    """Sets metric times from a list of possible metric column names.  Can set for whole warehouse or for a list of
    table IDs."""
    client = cli_client_factory(bigeye_conf, config_file, workspace)

    if warehouse_id and table_ids:
        raise Exception('Must include either table IDs OR warehouse ID OR schema ID.')
    elif warehouse_id or schema_id:
        client.set_source_metric_times(column_names=metric_column_names, wid=warehouse_id, sid=schema_id,
                                       replace=replace_set_metric_times)
    elif table_ids:
        client.set_table_metric_times(column_names=metric_column_names, table_ids=table_ids,
                                      replace=replace_set_metric_times)
    else:
        raise Exception('Must include either table IDs OR warehouse ID OR schema ID.')


@app.command()
def unset_metric_time(
        bigeye_conf: str = global_options.bigeye_conf,
        config_file: str = global_options.config_file,
        workspace: str = global_options.workspace,
        warehouse_id: int = typer.Option(
            None
            , "--warehouse_id"
            , "-wid"
            , help="Warehouse ID"),
        table_ids: Optional[List[int]] = typer.Option(
            None
            , "--table_id"
            , "-tid"
            , help="List of table IDs.")
):
    """Unsets metric times for whole warehouse or for a list og table IDs."""
    client = cli_client_factory(bigeye_conf, config_file, workspace)

    if warehouse_id and table_ids:
        raise Exception('Must include either table IDs OR warehouse id.')
    elif warehouse_id:
        client.unset_source_metric_times(wid=warehouse_id)
    elif table_ids:
        client.unset_table_metric_times(table_ids=table_ids)
    else:
        raise Exception('Must include either table IDs OR warehouse id.')


@app.command()
def get_metric_queries(
        bigeye_conf: str = global_options.bigeye_conf,
        config_file: str = global_options.config_file,
        workspace: str = global_options.workspace,
        warehouse_id: int = typer.Option(
            None
            , "--warehouse_id"
            , "-wid"
            , help="Warehouse ID"),
        schema_names: Optional[List[str]] = typer.Option(
            None
            , "--schema_name"
            , "-sn"
            , help="List of Schema Names.  E.g. -sn schema_1 -sn schema_2."),

        table_ids: Optional[List[int]] = typer.Option(
            None
            , "--table_id"
            , "-tid"
            , help="Table IDs.  E.g. -tid 123 -tid 124"),
        output_path: str = typer.Option(
            ...
            , "--output_path"
            , "-op"
            , help="File to write the failed metric configurations to.")
):
    """Gets the debug queries for all metrics by warehouse id, schema names, or table ids."""
    client = cli_client_factory(bigeye_conf, config_file, workspace)

    mil: MetricInfoList = client.get_metric_info_batch_post(warehouse_ids=[warehouse_id],
                                                            table_ids=table_ids)
    if schema_names:
        mil.metrics = [m for m in mil.metrics if m.metric_metadata.schema_name in schema_names]

    mids = [m.metric_configuration.id for m in mil.metrics]

    r = client.get_debug_queries(metric_ids=mids)

    write_debug_queries(output_path=output_path, queries=r)


@app.command()
def upsert_template(
        bigeye_conf: str = global_options.bigeye_conf,
        config_file: str = global_options.config_file,
        workspace: str = global_options.workspace,
        source_name: str = typer.Option(
            ...
            , "--source_name"
            , "-sn"
            , help="The name of the source where the template will be defined"),
        template_name: str = typer.Option(
            ...
            , "--name"
            , "-tn"
            , help="The user defined name of the template"),
        template_body: str = typer.Option(
            ...
            , "--body"
            , "-tb"
            , help="The string to define the template"),
        return_type: SimpleMetricTemplateFieldType = typer.Option(
            ...
            , "--returns"
            , "-rt"
            , help="The data type returned by the template; i.e. NUMERIC, BOOLEAN"),
        # TODO: Update to List[Tuple[str, SimpleMetricTemplateParameterType]] when supported by typer.
        parameters: List[str] = typer.Option(
            ...
            , "--params"
            , "-p"
            , help="A list of key/value pairs for parameters; ex. -p column=COLUMN_REFERENCE -p table=STRING"),
        template_id: Optional[int] = typer.Option(
            0
            , "--template_id"
            , "-id"
            , help="The template ID (Only required when updating a template)."
        )
):
    """Create or update a template for a source."""
    # TODO: Lookup template ID, once template names are unique
    client = cli_client_factory(bigeye_conf, config_file, workspace)

    source: Source = [s for s in client.get_sources().sources if s.name == source_name][0]
    log.info(f"Creating metric template in warehouse {source.name}")
    r = client.upsert_metric_template(id=template_id,
                                      name=template_name,
                                      template=template_body,
                                      return_type=return_type,
                                      parameters=parameters,
                                      source=source)
    log.info(f"Upsert for metric template complete:\n\tID:{r.metric_template.id}\n\tName:{r.metric_template.name}\n\t")


@app.command()
def get_all_metric_templates(
        bigeye_conf: str = global_options.bigeye_conf,
        config_file: str = global_options.config_file,
        workspace: str = global_options.workspace,
        page_size: Optional[int] = typer.Option(
            0
            , "--page_size"
            , "-ps"
            , help="How many results to return per page"
        ),
        search: Optional[str] = typer.Option(
            ""
            , "--search"
            , "-s"
            , help="A search string to narrow results"
        ),
        output_path: str = typer.Option(
            None
            , "--output_path"
            , "-op"
            , help="The path to output templates"
        ),
        file_name: Optional[str] = typer.Option(
            None
            , "--file_name"
            , "-fn"
            , help="User defined file name"
        )
):
    """Retrieve all metric templates and output to a file."""
    client = cli_client_factory(bigeye_conf, config_file, workspace)
    metric_templates = client.get_all_metric_templates(page_size=page_size, search=search)
    if not output_path:
        output_path = Path.cwd()

    write_metric_templates(output_path=output_path, metric_templates=metric_templates, file_name=file_name)


@app.command()
def delete_template(
        bigeye_conf: str = global_options.bigeye_conf,
        config_file: str = global_options.config_file,
        workspace: str = global_options.workspace,
        template_id: int = typer.Option(
            ...
            , "--template_id"
            , "-tid"
            , help="The ID of the metric template")
):
    """Delete a template."""
    client = cli_client_factory(bigeye_conf, config_file, workspace)
    client.delete_metric_template(template_id=template_id)
    log.info(f"Template ID {template_id} deleted.")


@app.command()
def upsert_virtual_table(
        bigeye_conf: str = global_options.bigeye_conf,
        config_file: str = global_options.config_file,
        workspace: str = global_options.workspace,
        virtual_table_name: str = typer.Option(
            ...
            , "--table_name"
            , "-vtn"
            , help="The name of the virtual table"),
        sql: str = typer.Option(
            ...
            , "--sql"
            , "-s"
            , help="The SQL to define the table"),
        source_name: str = typer.Option(
            ...
            , "--source_name"
            , "-sn"
            , help="The name of the source where the virtual table will be defined"),
        update: bool = typer.Option(
            False
            , "--update"
            , "-u"
            , help="Create if false. Update if true.")
):
    """Create or update a virtual table."""
    client = cli_client_factory(bigeye_conf, config_file, workspace)

    source: Source = [s for s in client.get_sources().sources if s.name == source_name][0]

    if update:
        log.warning(f"The update flag has been deprecated. This command will now scan for virtual tables that match the"
                    f"given source and virtual table names. If one is found, the virtual table will be updated, "
                    f"else the virtual table will be created.")

    table: Table = next(
        (vt.table for vt in client.get_all_virtual_tables() if vt.table.warehouse_id == source.id and
         vt.table.name == virtual_table_name), None)

    if table:
        log.info(f"Update {table.name} in warehouse {source.name}")
        client.update_virtual_table(id=table.id, name=virtual_table_name, sql=sql, warehouse_id=source.id)
    else:
        log.info(f"Creating virtual table {virtual_table_name} in warehouse {source.name}")
        client.create_virtual_table(name=virtual_table_name, sql=sql, warehouse_id=source.id)


@app.command()
def delete_virtual_table(
        bigeye_conf: str = global_options.bigeye_conf,
        config_file: str = global_options.config_file,
        workspace: str = global_options.workspace,
        virtual_table_name: str = typer.Option(
            ...
            , "--table_name"
            , "-vtn"
            , help="The name of the virtual table"),
        source_name: str = typer.Option(
            ...
            , "--source_name"
            , "-sn"
            , help="The name of the source where the template will be defined")
):
    """Delete a virtual table."""
    client = cli_client_factory(bigeye_conf, config_file, workspace)
    source: Source = [s for s in client.get_sources().sources if s.name == source_name][0]
    table: Table = [vt for vt in client.get_all_virtual_tables() if vt.table.warehouse_id == source.id and
                    vt.table.name == virtual_table_name][0].table

    client.delete_virtual_table(table_id=table.id)
