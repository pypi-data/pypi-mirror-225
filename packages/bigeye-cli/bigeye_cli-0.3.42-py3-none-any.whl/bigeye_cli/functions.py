import enum
import os
from typing import List, Dict
import typer
from rich.prompt import Prompt

from bigeye_sdk.class_ext.enum_ext import StrEnum
from bigeye_sdk.client.datawatch_client import DatawatchClient, datawatch_client_factory, get_user_auth
from bigeye_sdk.functions.metric_functions import get_file_name_for_metric
from bigeye_sdk.functions.file_functs import create_subdir_if_not_exists, serialize_listdict_to_json_file, \
    write_to_file, serialize_list_to_json_file
from bigeye_sdk.functions.helpers import str_to_bool
from bigeye_sdk.log import get_logger
from bigeye_sdk.authentication.api_authentication import ApiAuth
from bigeye_sdk.authentication.config import Config, WorkspaceConfig
from bigeye_sdk.exceptions.exceptions import WorkspaceNotSetException, ConfigNotFoundException
from bigeye_sdk.generated.com.bigeye.models.generated import MetricInfoList, Table, Issue, MetricTemplate
from bigeye_sdk.model.protobuf_extensions import MetricDebugQueries

log = get_logger(__file__)


def print_txt_file(file: str):
    from rich.console import Console

    console = Console()
    with open(file, "r+") as help_file:
        with console.pager():
            console.print(help_file.read())


def print_markdown(file: str):
    from rich.console import Console
    from rich.markdown import Markdown

    console = Console()
    with open(file, "r+") as help_file:
        with console.pager():
            console.print(Markdown(help_file.read()))


def cli_client_factory(auth_file: str = None, config_file: str = None, workspace: str = 'DEFAULT') -> DatawatchClient:
    """
    Args:
        auth_file: file containing the credentials.  If none will look for environment var BIGEYE_API_CRED_FILE
        or the default cred file.
        config_file: file containing cli configuration. If none will look for environment var BIGEYE_CONFIG_FILE 
        or the default config file at ~/.bigeye/config
        workspace: the workspace to execute all client requests from. If none will default to the workspace id provided
        in the default section of the config file.

    Returns: a Datawatch client

    """

    # Attempt to initialize client with new config process, if user has not run bigeye configure yet, fallback to
    # old approach only if they still only have access to 1 workspace.
    try:
        # Create instances of api auth and config classes
        config = Config.load_config(config_file)
        use_default_credential = str_to_bool(config[workspace]['use_default_credential'])
        if use_default_credential:
            auth = ApiAuth.load(auth_file=auth_file, workspace='DEFAULT')
        else:
            auth = ApiAuth.load(auth_file=auth_file, workspace=workspace)


        # Attempt to get workspace configuration. If no config created yet, then throw an error 
        # and have the user run the bigeye configure command.
        try:
            workspace_config = WorkspaceConfig(**config[workspace])
        except Exception:
            raise WorkspaceNotSetException(f'No workspace named {workspace} found in config file. Try '
                                           f'running bigeye configure -w {workspace} command to set '
                                           'workspace config settings.')

    except ConfigNotFoundException:
        log.warning(f'Config file not found. Please run the bigeye configure command.')
        auth = ApiAuth.load(auth_file=auth_file, workspace='DEFAULT')
        accessible_workspaces = get_user_auth(auth).workspaces
        if len(accessible_workspaces) == 1:
            # User has access to only 1 workspace, fallback to that
            log.info(f"No workspace provided, defaulting to only valid workspace: {accessible_workspaces[0].name}")
            return datawatch_client_factory(auth=auth, workspace_id=accessible_workspaces[0].id)

        elif len(accessible_workspaces) > 1:
            # User has access to more than 1 workspace, need to confirm correct one
            raise ConfigNotFoundException(f"No config files found. Please run the bigeye configure command.")
        else:
            # User has access to no workspaces - throw an error to let them know
            raise WorkspaceNotSetException(f'No workspace access detected. Please check with your Bigeye '
                                           'administrators to obtain access to a workspace.')

    return datawatch_client_factory(auth=auth, workspace_config=workspace_config)


def write_metric_info(output_path: str, metrics: MetricInfoList,
                      file_name: str = None, only_metric_conf: bool = False):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    for metric in metrics.metrics:
        """Writes individual metrics to files in the output path."""
        mc = metric.metric_configuration
        md = metric.metric_metadata

        if only_metric_conf:
            datum = mc
            log.info('Persisting metric configurations.')
        else:
            datum = metric
            log.info('Persisting metric info.')

        if not file_name:
            subpath = f"{output_path}/metric_info/warehouse_id-{md.warehouse_id}"

            create_subdir_if_not_exists(path=subpath)
            fn = get_file_name_for_metric(metric)
            url = f'{subpath}/{fn}'
        else:
            url = f'{output_path}/metric_info/{file_name}'

        serialize_listdict_to_json_file(url=url,
                                        data=[datum.to_dict()])


def write_debug_queries(output_path: str, queries: List[MetricDebugQueries]):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    for q in queries:
        subpath = f"{output_path}/debug_queries"

        create_subdir_if_not_exists(path=subpath)

        fn = f'{q.metric_id}_metric_query.txt'
        url = f'{subpath}/{fn}'
        write_to_file(url, [q.debug_queries.metric_query])

        if q.debug_queries.debug_query:
            fn = f'{q.metric_id}_debug_query.txt'
            url = f'{subpath}/{fn}'
            write_to_file(url, [q.debug_queries.debug_query])


def write_table_info(output_path: str, tables: List[Table], file_name: str = None):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    for table in tables:
        """Writes individual issues to files in the output path."""
        log.info('Persisting issue.')
        if not file_name:
            subpath = f"{output_path}/table_info/warehouse_id-{table.warehouse_id}"

            create_subdir_if_not_exists(path=subpath)
            fn = f'{table.id}-{table.schema_name}-{table.name}.json'
            url = f'{subpath}/{fn}'
        else:
            url = f'{output_path}/{file_name}'

        serialize_listdict_to_json_file(url=url,
                                        data=[table.to_dict()])


def write_issue_info(output_path: str, issues: List[Issue], file_name: str = None):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    for issue in issues:
        """Writes individual issues to files in the output path."""
        log.info('Persisting issue.')
        if not file_name:
            subpath = f"{output_path}/issue_info/warehouse_id-{issue.metric_configuration.warehouse_id}" \
                      f"/dataset_id-{issue.metric_configuration.dataset_id}" \
                      f"/{issue.metric_configuration.name.replace(' ', '_')}"

            create_subdir_if_not_exists(path=subpath)
            fn = f'{issue.id}-{issue.name}.json'
            url = f'{subpath}/{fn}'
        else:
            url = f'{output_path}/{file_name}'

        serialize_listdict_to_json_file(url=url,
                                        data=[issue.to_dict()])


def write_metric_templates(output_path: str, metric_templates: List[MetricTemplate], file_name: str = None):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    if not file_name:
        file_name = "metric_templates.json"

    url = f'{output_path}/{file_name}'

    serialize_list_to_json_file(url=url, data=metric_templates)


def run_enum_menu(enum_clz: enum.EnumMeta, default: StrEnum) -> StrEnum:
    valid_types: Dict[int, StrEnum] = {index: auth_type for index, auth_type in enumerate(list(enum_clz), start=1)}
    valid_type_by_type: Dict[StrEnum, int] = {v: k for k, v in valid_types.items()}

    user_chosen_type_ix = 0

    while user_chosen_type_ix not in valid_type_by_type.values():
        for user_chosen_type_ix, index in valid_type_by_type.items():
            typer.echo(f"{index}) {user_chosen_type_ix.value}")
        try:
            user_chosen_type_ix = int(Prompt.ask(
                f"Which authorization method would you like to use? "
                f"(Default: {valid_type_by_type[default]})", default=valid_type_by_type[default])
            )
        except ValueError as e:
            pass

        if user_chosen_type_ix not in valid_types.keys():
            typer.echo(f"Invalid Choice.")

    return valid_types[user_chosen_type_ix]
