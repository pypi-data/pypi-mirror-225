import click
from rich.text import Text

from patch.auth.auth_token import global_access_token
from patch.cli.commands import pass_obj, with_as_tenant
from patch.cli.styled import StyledGroup, StyledCommand
from patch.cli.tools.connectors.connector_spec import ConnectorConfigSpec


@click.group(cls=StyledGroup, help='Review the requirements to connect to supported data sources',
             hidden=not global_access_token.has_token())
@click.pass_context
def connector(_ctx, ):
    pass


@connector.group(cls=StyledGroup, help='Connectivity commands for Snowflake')  # List of sources that Patch can observe
def snowflake():
    pass


@connector.group(cls=StyledGroup, help='Connectivity commands for BigQuery')
def bigquery():
    pass


@connector.group(cls=StyledGroup, help='Connectivity commands for Azure Blob Storage')
def azure_blob():
    pass


@azure_blob.command(cls=StyledCommand, help='Fields required for connection to Azure Blob Storage')
@pass_obj()
def spec(patch_ctx):
    console = patch_ctx.console
    connector_spec = ConnectorConfigSpec('azure-blob')
    table = connector_spec.render_connector_spec()
    console.print(table)


@bigquery.command(cls=StyledCommand, help='Fields required for connection to BigQuery')
@pass_obj()
def spec(patch_ctx):
    console = patch_ctx.console
    connector_spec = ConnectorConfigSpec('bigquery')
    table = connector_spec.render_connector_spec()
    console.print(table)


@snowflake.command(cls=StyledCommand, help='Fields required for connection to Snowflake')
@pass_obj()
def spec(patch_ctx):
    console = patch_ctx.console
    connector_spec = ConnectorConfigSpec('snowflake')
    table = connector_spec.render_connector_spec()
    console.print(table)


@snowflake.command(cls=StyledCommand, help='Get RSA public key for Keypair Auth',
                   hidden=not global_access_token.has_token())
@click.option('-s', '--silent', help='Do not print instructions', is_flag=True)
@with_as_tenant()
@pass_obj()
def get_patch_public_key(patch_ctx, silent):
    console = patch_ctx.console
    client = patch_ctx.gql_client
    gql_query = client.prepare_query('sharing')
    share_result = gql_query.execute()
    pub_key = share_result.snowflake.publicKey
    if silent:
        console.out(pub_key)
    else:
        console.print(f"Public key:")
        console.out(Text.from_markup(f"[green]{pub_key}[/green]"), style='green')
        console.print("")
        console.print("[yellow]Hint:[/yellow]")
        console.print("If you have a Snowflake database that you want to connect Patch to, run the following")
        console.print("in that database to enable Patch to authenticate with Snowflake using an RSA key.")
        console.print("")
        console.out(f"    ALTER USER patch_user SET RSA_PUBLIC_KEY = '{pub_key}';", style='white')
