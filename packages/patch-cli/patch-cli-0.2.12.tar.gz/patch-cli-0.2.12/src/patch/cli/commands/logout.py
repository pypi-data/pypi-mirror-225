import click
from patch.auth.auth_token import global_access_token
from patch.cli.styled import StyledCommand
from patch.cli.commands import pass_obj
from patch.cli import PatchClickContext


@click.command(cls=StyledCommand, help='Logout',
               hidden=not global_access_token.has_token())
@pass_obj()
def logout(patch_ctx: PatchClickContext):
    console = patch_ctx.console
    if global_access_token:
        global_access_token.delete()
    console.print("Logged out [green]successfully[/green]")
