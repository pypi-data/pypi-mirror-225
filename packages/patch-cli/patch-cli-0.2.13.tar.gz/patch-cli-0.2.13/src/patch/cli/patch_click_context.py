import click
import os
import ssl
import urllib
from rich.console import Console
from patch.gql.client import Client
from typing import Optional


class PatchClickContext:

    def __init__(self, *, click_ctx: click.Context, terminal_width: Optional[int], allow_insecure: Optional[bool]):
        self._click_ctx = click_ctx
        self._console = Console(width=terminal_width)
        self._allow_insecure = allow_insecure
        self._endpoint = os.environ.get('PATCH_ENDPOINT')
        if self._endpoint is None or self._endpoint == "":
            self._endpoint = "https://api.patch.tech"
        # If allow_insecure, use an unverified context.
        # Else, use the system (OpenSSL) context.
        self._ssl_context = ssl._create_unverified_context() if allow_insecure  else ssl.create_default_context()
        self._urlopen = lambda url, **kwargs: urllib.request.urlopen(url, context=self._ssl_context, **kwargs)

    @property
    def console(self):
        return self._console

    def exit(self, code=0):
        """
        Exits the application with a given exit code.
        Exit nonzero only for errors, not warnings.
        """
        self._click_ctx.exit(code)

    def switch_to_data_output(self) -> Console:
        """Switch default console to stderr and return the original console
        to stdout. Call this when preparing to output data that users may
        want to redirect to text-processing tools."""
        if self._console.stderr:
            raise RuntimeError('Method called more than once.')

        stdout_console = self._console
        self._console = Console(stderr=True)
        return stdout_console

    @property
    def gql_client(self):
        params = click.get_current_context().params
        as_tenant = params.get('as_tenant', None) if params else None
        return Client(self, as_tenant=as_tenant)

    @property
    def patch_endpoint(self):
        return self._endpoint

    @property
    def ssl_context(self):
        return self._ssl_context

    @property
    def urlopen(self):
        return self._urlopen
