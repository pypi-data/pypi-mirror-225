import click
from patch.auth.auth_token import global_access_token
from rich.table import Table
from patch.cli import PatchClickContext
from patch.cli.commands import pass_obj
from patch.cli.styled import StyledCommand
from patch.cli.styled import NONE_BOX
from patch.cli.tools.tables.renders import render_number
from patch.cli.commands import active_source
from patch.cli.commands import with_as_tenant


def render_current_user(current_user, local_state):
    tenant = current_user.tenant
    table = Table(title='Current user', show_edge=True, box=NONE_BOX, show_header=False)
    table.add_column("", style="white")
    table.add_column("", style="cyan")
    table.add_row('Name', current_user.fullName)
    table.add_row('ID', f"[yellow]{current_user.id}[/yellow]")
    table.add_row('Login', current_user.login)
    table.add_row('Tenant name', tenant.name)
    table.add_row('Tenant ID', f"[yellow]{tenant.id}[/yellow]")
    quota_str = render_number(tenant.quota, 1024, ['', 'KB', 'MB', 'GB', 'TB'])
    table.add_row('Quota', quota_str)
    active_source_name = local_state.active_source_name if local_state else ""
    if active_source_name:
        rendered_source = f"[green]{active_source_name}[/green]"
    else:
        rendered_source = f"[white][dim](none)[/dim][/white]"
    table.add_row('Local state', rendered_source)
    return table


@click.command(cls=StyledCommand, help='Returns details about the current user',
               hidden=not global_access_token.has_token())
@with_as_tenant()
@pass_obj()
def user(patch_ctx: PatchClickContext):
    console = patch_ctx.console
    with active_source(patch_ctx, show_state=False, err_if_none=False) as local_state:
        client = patch_ctx.gql_client
        q = client.prepare_query('currentUser')
        current_user = q.execute()
        table = render_current_user(current_user, local_state)
        console.print(table)
