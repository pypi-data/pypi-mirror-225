import click
from rich.console import Console

from patch.auth.auth_client import AuthClient
from patch.auth.auth_token import global_access_token
from patch.cli import PatchClickContext
from patch.cli.commands import pass_obj
from patch.cli.styled import StyledCommand


@click.command(cls=StyledCommand, help='Patch API access token (deprecated, use: pat access token)',
               hidden=not global_access_token.has_token())
@pass_obj()
def token(patch_ctx: PatchClickContext):
    console_err = Console(stderr=True)
    console_err.print("[red]This command is deprecated. Please use: pat access token[/red]")
    console = patch_ctx.console
    auth_client = AuthClient(patch_ctx)
    access_token = auth_client.get_access_token()
    if not access_token:
        console.print("[red]Error[/red] You need to log-in!")
        patch_ctx.exit(1)
    else:
        click.echo(access_token)
