from contextlib import contextmanager
from functools import update_wrapper
from typing import Generator

import click
import os

from patch.auth.auth_token import global_is_admin_or_mta
from patch.cli import PatchClickContext
from patch.cli.remote.source_client import SourceClient
from patch.cli.styled import colorize
from patch.storage.state_file import StatePayload
from patch.storage.storage import Storage


@contextmanager
def active_source(patch_ctx: PatchClickContext,
                  show_state=False,
                  err_if_none=True) -> Generator[StatePayload, None, None]:
    console = patch_ctx.console
    storage = Storage()
    state = storage.source_state
    if not state.exists():
        sc = SourceClient(patch_ctx.gql_client)
        sources = sc.get_sources()
        if len(sources) == 1:
            source = sources[0]
            state_payload = StatePayload(active_source_id=source.id, active_source_name=source.name)
            state.store(state_payload)
            yield state_payload
        else:
            if err_if_none:
                raise click.ClickException(colorize(console, 'No active source', style='red') + "\n" +
                                           f"Call {colorize(console, 'pat source use <name>', style='yellow')}" +
                                           f" for selecting active source")
            else:
                yield None
    else:
        loaded = state.load()
        if show_state:
            console.print(f"Active source: [green]{loaded.active_source_name}[/green]")
        yield loaded


def pass_obj():
    def inner(func):
        @click.pass_context
        def wrapper(ctx, *args, **kwargs):
            return ctx.invoke(func, ctx.obj, *args, **kwargs)

        return update_wrapper(wrapper, func)

    return inner


def with_as_tenant():
    def inner(func):
        @click.option('--as-tenant',
                      help='Tenant ID. Execute command on behalf of this tenant',
                      expose_value=True,
                      default=os.environ.get('PATCH_TENANT'),
                      hidden=not global_is_admin_or_mta)
        @click.pass_context
        def wrapper(ctx, as_tenant, *args, **kwargs):
            return ctx.invoke(func, *args, **kwargs)

        return update_wrapper(wrapper, func)

    return inner
