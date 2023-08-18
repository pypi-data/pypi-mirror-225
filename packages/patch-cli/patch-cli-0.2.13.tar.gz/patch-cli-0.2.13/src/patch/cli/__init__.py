import click
import os
import sys

from patch.auth.auth_token import global_is_admin_or_mta
from patch.cli.patch_click_context import PatchClickContext
from patch.debug import debug_enabled
from patch.cli.commands.alpha import alpha
from patch.cli.commands.connector import connector
from patch.cli.commands.login import login
from patch.cli.commands.logout import logout
from patch.cli.commands.source import source
from patch.cli.commands.dataset import dataset
from patch.cli.commands.dataset import edge
from patch.cli.commands.destination import destination
from patch.cli.commands.admin import admin
from patch.cli.commands.playground import playground
from patch.cli.commands.token import token
from patch.cli.commands.user import user
from patch.cli.commands.access import access
from rich.console import Console

from patch.cli.eap import eap_warning
from patch.cli.styled import StyledGroup


def safe_main():
    try:
        main()
    except Exception as e:
        console = Console(stderr=True)
        console.print(f"[red]error: {e}[/red]")
        if debug_enabled():
            console.print_exception()
        sys.exit(1)


@click.group(cls=StyledGroup)
@click.pass_context
@click.option("--allow-insecure", is_flag=True, default=False, help="Accept invalid HTTPS certificates")
def main(ctx, allow_insecure):
    ctx.ensure_object(dict)
    ctx.obj = PatchClickContext(click_ctx=ctx, terminal_width=ctx.terminal_width, allow_insecure=allow_insecure)


if global_is_admin_or_mta:
    main.add_command(alpha)
main.add_command(login)
main.add_command(logout)
main.add_command(user)
main.add_command(connector)
main.add_command(source)
main.add_command(destination)
main.add_command(dataset)
main.add_command(edge)
main.add_command(admin)
main.add_command(playground)
main.add_command(token)
main.add_command(access)
