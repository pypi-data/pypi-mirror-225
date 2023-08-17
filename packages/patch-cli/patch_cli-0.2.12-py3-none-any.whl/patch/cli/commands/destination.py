import click
import json
from rich.prompt import Confirm
from rich import box
from rich.table import Table

from patch.auth.auth_token import global_access_token
from patch.cli import PatchClickContext
from patch.cli.commands import pass_obj, with_as_tenant
from patch.cli.styled import StyledGroup, StyledCommand
from patch.cli.tools.config_interactive import ConfigInteractive
from patch.cli.tools.config_non_interactive import ConfigNonInteractive
from patch.cli.tools.destinations.destination_spec import field_specs, DestinationConfigSpec


@click.group(cls=StyledGroup, help='Create or remove Warehouse API destinations for polling batch data.',
             hidden=not global_access_token.has_token())
def destination():
    pass

@destination.command(cls=StyledCommand, help='Create a destination')
@click.option('-c', '--config', type=click.File(mode='r'), help='Configuration file')
@click.option('-i', '--interactive', help='Interactive mode', is_flag=True)
@with_as_tenant()
@pass_obj()
def create(patch_ctx: PatchClickContext, config, interactive):
    console = patch_ctx.console
    if not config and not interactive:
        console.print("[red]Provide either configuration file or interactive mode[/red]")
        patch_ctx.exit(1)
    if interactive:
        destination_config = ConfigInteractive(console, config)
    else:
        destination_config = ConfigNonInteractive(config)
    config_values = destination_config.resolve_config(field_specs)
    result_dest = destination_config.send_to_gql(patch_ctx, config_values, spec=DestinationConfigSpec)
    console.print(f"[green]Succeeded[/green]")
    console.print(f"Destination Name: [yellow]{result_dest.name}[/yellow]")      


@destination.command(cls=StyledCommand, help='Remove a destination')
@click.argument('name', type=click.STRING)
@click.option('-y', '--assume-yes', '--yes', help='Skip confirmation', is_flag=True)
@with_as_tenant()
@pass_obj()
def remove(patch_ctx: PatchClickContext, name, assume_yes):
    console = patch_ctx.console
    confirmation = assume_yes or Confirm.ask(f"Would you like to remove Destination [cyan]{name}[/cyan]?",
                                             console=console)
    if confirmation:
        client = patch_ctx.gql_client
        gql_mutation = client.prepare_mutation('removeDestination', input={'name': name})
        gql_mutation.execute()
        console.print(f"[green]Destination queued for deletion[/green]")
    else:
        console.print(f"Command [red]aborted[/red]")


@destination.command(cls=StyledCommand, help='List destinations', aliases=['list'])
@with_as_tenant()
@pass_obj()
def ls(patch_ctx: PatchClickContext):
    console = patch_ctx.console
    client = patch_ctx.gql_client
    gql_query = client.prepare_query('destinations')
    with gql_query as q:
        q.__fields__('name', 'type', 'batchApi')
    destination_list = gql_query.execute()

    if not destination_list:
        console.print("[yellow]No destinations found[/yellow]")
    else:
        table = Table(title="Destinations", box=box.ROUNDED, border_style="grey37")
        table.add_column("Name", style="cyan", no_wrap=True, overflow="fold")
        table.add_column("Type", style="yellow", overflow="fold")

        destination_list_sorted = sorted(destination_list, key=lambda d: d.name.lower())
        for destination_elem in destination_list_sorted:
            table.add_row(destination_elem.name, destination_elem.type)

        console.print(table)
