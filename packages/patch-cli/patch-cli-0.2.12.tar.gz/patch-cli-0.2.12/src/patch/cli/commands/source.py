import click

from patch.auth.auth_token import global_access_token
from patch.cli import PatchClickContext
from patch.cli.remote.source_client import SourceClient
from patch.cli.styled import StyledGroup, StyledCommand
from patch.cli.commands import pass_obj, with_as_tenant
from patch.cli.tools.config_interactive import ConfigInteractive
from patch.cli.tools.connectors.connector_spec import field_specs, ConnectorConfigSpec
from patch.cli.tools.config_non_interactive import ConfigNonInteractive

from rich import box
from rich.table import Table
from rich.prompt import Confirm

from patch.storage.state_file import StatePayload
from patch.storage.storage import Storage


@click.group(cls=StyledGroup, help='Connect, disconnect, and use sources to create datasets',
             hidden=not global_access_token.has_token())
def source():
    pass


@source.command(cls=StyledCommand, help='Provide source configuration')
@click.option('-c', '--config', type=click.File(mode='r'), help='Configuration file')
@click.option('-i', '--interactive', help='Interactive mode', is_flag=True)
# TODO(PAT-2393): Move --staging-db from here to a Snowflake-only path
@click.option('-s', '--staging-db', help='(Snowflake Only) Name of the staging database')
@with_as_tenant()
@pass_obj()
def connect(patch_ctx: PatchClickContext, config, interactive, staging_db):
    console = patch_ctx.console
    if not config and not interactive:
        console.print("[red]Provide either configuration file or interactive mode[/red]")
        patch_ctx.exit(1)
    if interactive:
        source_config = ConfigInteractive(console, config, staging_db)
    else:
        source_config = ConfigNonInteractive(config, staging_db)
    config_values = source_config.resolve_config(field_specs)

    result_source = source_config.send_to_gql(patch_ctx, config_values, spec=ConnectorConfigSpec)
    console.print(f"[green]Succeeded[/green]")
    console.print(f"Source Name: [yellow]{result_source.name}[/yellow], ID [yellow]{result_source.id}[/yellow]")


@source.command(cls=StyledCommand, help='Disconnect source from Patch')
@click.argument('name', type=click.STRING)
@click.option('-y', '--assume-yes', '--yes',
              help='Skip confirmation, will fail if datasets are still attached to source', is_flag=True)
@with_as_tenant()
@pass_obj()
def disconnect(patch_ctx: PatchClickContext, name, assume_yes):
    console = patch_ctx.console
    confirmation = assume_yes or Confirm.ask(f"Would you like to remove Source [cyan]{name}[/cyan]? ", console=console)
    if confirmation:
        client = patch_ctx.gql_client
        mut = client.prepare_mutation('sourceDisconnect', input={'name': name})
        mut.execute()
        console.print(f"[green]Succeeded[/green]")
        # As a secondary step delete the local default if it's the same one that was disconnected
        source_storage = Storage().source_state
        if source_storage.exists() and name == source_storage.load().active_source_name:
            source_storage.delete()
    else:
        console.print(f"Command [red]aborted[/red]")


@source.command(cls=StyledCommand, help='Check if Patch can connect to your source')
@click.argument('name', type=click.STRING, required=False)
@with_as_tenant()
@pass_obj()
def status(patch_ctx: PatchClickContext, name):
    console = patch_ctx.console
    if not name:
        storage = Storage()
        if storage.source_state.exists():
            state = storage.source_state.load()
            name = state.active_source_name
        else:
            console.print('[red]No name or default provided, use "pat source use" to set default[/red]')
            patch_ctx.exit(4)
            return
    client = patch_ctx.gql_client
    q = client.prepare_query('getSourceStatus', input={'name': name})
    q.execute()
    console.print(f"[green]{name} status: OK[/green]")


@source.command(cls=StyledCommand, help='List sources', aliases=['list'])
@with_as_tenant()
@pass_obj()
def ls(patch_ctx: PatchClickContext):
    console = patch_ctx.console
    client = SourceClient(patch_ctx.gql_client)
    source_list = client.get_sources()
    if not source_list:
        console.print("[yellow]No sources found[/yellow]")
    else:
        table = Table(title="Sources", box=box.ROUNDED, border_style="grey37")
        table.add_column("Name", justify="left", style="cyan", no_wrap=True)
        table.add_column("ID", justify="left", style="yellow", no_wrap=True)
        sorted_sources = sorted(source_list, key=lambda s: s.name)
        for source_elem in sorted_sources:
            table.add_row(source_elem.name, source_elem.id)
        console.print(table)


@source.command(cls=StyledCommand, help='Select this source as default one')
@click.argument('name', type=click.STRING)
@click.option('-f', '--force', help='Select this source as default even if connection fails ', is_flag=True)
@with_as_tenant()
@pass_obj()
def use(patch_ctx: PatchClickContext, name, force):
    console = patch_ctx.console
    client = SourceClient(patch_ctx.gql_client)
    result_q = client.get_sources_by_name(name)
    result_q_len = len(result_q)
    if result_q_len == 0:
        console.print(f"[red]Unknown source name[/red]")
        patch_ctx.exit(2)
    elif result_q_len > 1:
        console.print(f"[red]More than one source with this name[/red]")
        patch_ctx.exit(3)
    else:
        result_source = result_q[0]
        if not force:
            # Check if source credentials are correct
            client.check_source_connectable(name)
        storage = Storage()
        storage.source_state.store(StatePayload(
            active_source_name=result_source.name, active_source_id=result_source.id))
        console.print(f"Stored [cyan]{result_source.name}[/cyan], ID: [yellow]{result_source.id}[/yellow]")
