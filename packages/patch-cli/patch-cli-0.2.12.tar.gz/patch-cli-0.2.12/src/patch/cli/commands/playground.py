import json
import click
from patch.auth.auth_client import AuthClient
from patch.auth.auth_token import global_access_token
from patch.cli import PatchClickContext
from patch.cli.commands import pass_obj
from patch.cli.styled import StyledCommand
import pyperclip


@click.command(cls=StyledCommand, help='Launch GraphQL Playground',
                           hidden=not global_access_token.has_token())
@pass_obj()
def playground(patch_ctx: PatchClickContext):
    console = patch_ctx.console
    auth_client = AuthClient(patch_ctx)
    token = auth_client.get_access_token()
    if not token:
        console.print("[red]Error[/red] You need to log-in before you use GraphQL")
        patch_ctx.exit(1)
    else:
        gql_url = patch_ctx.gql_client.get_url()
        console.print("You are about to open GraphQL Playground.")
        console.print(
            "The configuration below will be copied to your clipboard. " +
            "You can paste it in [yellow]HTTP HEADERS[/yellow] tab in the Playground console.\n")
        headers = json.dumps({'Authorization': token})
        console.out(headers)
        console.print("\nExample query:")
        console.print("[blue]query[/blue] {")
        console.print("    [yellow]getSourceList[/yellow]([magenta]input[/magenta]:{}) { ")
        console.print("        [yellow]id [/yellow]")
        console.print("        [yellow]name[/yellow]")
        console.print("    } ")
        console.print("} ")

        console.input("\nPress Enter to continue...")
        result = click.launch(gql_url)
        if result != 0:
            console.input(f"Now, open [magenta]{gql_url}[/magenta]")
        else:
            console.print(f"If your default browser hasn't started open this page: [magenta]{gql_url}[/magenta]")
        pyperclip.copy(headers)
