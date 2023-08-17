from typing import Optional

import typer

from bigeye_cli.exceptions.exceptions import InvalidEntityException
from bigeye_cli.functions import cli_client_factory
from bigeye_cli import global_options
from bigeye_sdk.functions.table_functions import fully_qualified_table_to_elements
from bigeye_sdk.generated.com.bigeye.models.generated import Table, Integration
from bigeye_sdk.log import get_logger
from bigeye_sdk.model.protobuf_enum_facade import SimpleDataNodeType

log = get_logger(__file__)

app = typer.Typer(no_args_is_help=True, help='Lineage Commands for Bigeye CLI')

"""
File should contain commands relating to lineage calls to the API.
"""


@app.command()
def create_node(
        bigeye_conf: str = global_options.bigeye_conf,
        config_file: str = global_options.config_file,
        workspace: str = global_options.workspace,
        entity_name: str = typer.Option(
            ...
            , "--entity_name"
            , "-en"
            , help="The fully qualified table name or name of the tableau workbook"
        ),
        integration_name: Optional[str] = typer.Option(
            None
            , "--int_name"
            , "-in"
            , help="The name of the BI connection (required for entities outside of Bigeye)"
        )
):
    """Create a lineage node for an entity"""
    client = cli_client_factory(bigeye_conf,config_file,workspace)
    if not integration_name:
        warehouse, schema, entity_name = fully_qualified_table_to_elements(entity_name)
        table: Table = client.get_tables(schema=[schema], table_name=[entity_name]).tables[0]
        log.info(f"Creating lineage node for table: {entity_name}")
        entity_id = table.id
        node_type = SimpleDataNodeType.TABLE.to_datawatch_object()

    else:
        integration: Integration = [i for i in client.get_integrations() if i.name == integration_name][0]
        workbook = [w for w in client.get_integration_entities(integration_id=integration.id)
                    if w.name == entity_name][0]
        log.info(f"Creating lineage node for entity: {workbook.name}")
        entity_id = workbook.id
        node_type = SimpleDataNodeType.TABLEAU.to_datawatch_object()

    node = client.create_data_node(node_type=node_type, node_entity_id=entity_id)
    log.info(f"Node created:\n\tID: {node.id}\n\tname: {node.node_name}")


@app.command()
def delete_node(
        bigeye_conf: str = global_options.bigeye_conf,
        config_file: str = global_options.config_file,
        workspace: str = global_options.workspace,
        entity_name: str = typer.Option(
            ...
            , "--entity_name"
            , "-en"
            , help="The fully qualified table name or name of the tableau workbook"
        ),
        integration_name: Optional[str] = typer.Option(
            None
            , "--int_name"
            , "-in"
            , help="The name of the BI connection (required for entities outside of Bigeye)"
        )
):
    """Delete a lineage node for an entity"""
    client = cli_client_factory(bigeye_conf,config_file,workspace)
    if not integration_name:
        warehouse, schema, entity_name = fully_qualified_table_to_elements(entity_name)
        table: Table = client.get_tables(schema=[schema], table_name=[entity_name]).tables[0]
        log.info(f"Creating lineage node for table: {entity_name}")
        node_id = table.data_node_id

    else:
        integration: Integration = [i for i in client.get_integrations() if i.name == integration_name][0]
        workbook = [w for w in client.get_integration_entities(integration_id=integration.id)
                    if w.name == entity_name][0]
        log.info(f"Creating lineage node for entity: {workbook.name}")
        node_id = workbook.data_node_id

    client.delete_data_node(data_node_id=node_id)


@app.command()
def create_relation(
        bigeye_conf: str = global_options.bigeye_conf,
        config_file: str = global_options.config_file,
        workspace: str = global_options.workspace,
        upstream_table_name: str = typer.Option(
            ...
            , "--upstream"
            , "-up"
            , help="The fully qualified table name"
        ),
        downstream_table_name: str = typer.Option(
            ...
            , "--downstream"
            , "-down"
            , help="The fully qualified table name"
        )
):
    """Create a lineage relationship for 2 entities"""
    client = cli_client_factory(bigeye_conf,config_file,workspace)
    warehouse, u_schema, u_table_name = fully_qualified_table_to_elements(upstream_table_name)
    warehouse, d_schema, d_table_name = fully_qualified_table_to_elements(downstream_table_name)

    upstream: Table = client.get_tables(schema=[u_schema], table_name=[u_table_name]).tables[0]
    downstream: Table = client.get_tables(schema=[d_schema], table_name=[d_table_name]).tables[0]

    log.info(f"Creating relationship from {upstream_table_name} to {downstream_table_name}")

    r = client.create_table_lineage_relationship(upstream_data_node_id=upstream.data_node_id,
                                                 downstream_data_node_id=downstream.data_node_id)

    log.info(f"Relationship created:\n\tID: {r.id}\n\tupstream ID: {r.upstream.id}\n\tdownstream ID:{r.downstream.id}")


@app.command()
def delete_relation(
        bigeye_conf: str = global_options.bigeye_conf,
        config_file: str = global_options.config_file,
        workspace: str = global_options.workspace,
        entity_name: Optional[str] = typer.Option(
            None
            , "--entity_name"
            , "-en"
            , help="The fully qualified table name or name of the tableau workbook"
        ),
        relationship_id: Optional[int] = typer.Option(
            0
            , "--relation_id"
            , "-rid"
            , help="The relationship ID to delete"
        ),
        integration_name: Optional[str] = typer.Option(
            None
            , "--int_name"
            , "-in"
            , help="The name of the BI connection (required for entities outside of Bigeye)"
        )
):
    """Deletes a single relationship based on relation ID or all relationships for a node by name."""
    client = cli_client_factory(bigeye_conf,config_file,workspace)

    if not entity_name and not relationship_id:
        raise InvalidEntityException("No entity specified to delete.")
    elif relationship_id:
        client.delete_lineage_relationship(relationship_id=relationship_id)
    elif integration_name:
        integration: Integration = [i for i in client.get_integrations() if i.name == integration_name][0]
        workbook = [w for w in client.get_integration_entities(integration_id=integration.id)
                    if w.name == entity_name][0]
        log.info(f"Deleting all lineage relationships for entity: {workbook.name}")
        node_id = workbook.data_node_id
        client.delete_lineage_relationship_for_node(data_node_id=node_id)
    else:
        warehouse, schema, entity_name = fully_qualified_table_to_elements(entity_name)
        table: Table = client.get_tables(schema=[schema], table_name=[entity_name]).tables[0]
        log.info(f"Deleting all lineage relationships for table: {entity_name}")
        node_id = table.data_node_id
        client.delete_lineage_relationship_for_node(data_node_id=node_id)
