import json
import os
from typing import List, Optional

from rich.console import Console
from rich.table import Table

from patch.cli.styled import NONE_BOX
from patch.cli.tools.datasets.curl_renderer import has_curl, CurlRenderer
from patch.gql.schema import Dataset
from patch.storage.state_file import StatePayload

def table_route(name, primary_keys: List[str]):
    keys_path = ",".join(["{" + pk.lower() + "}" for pk in primary_keys])
    return f"/{name.lower()}/[yellow]{keys_path}[/yellow]"


def text_route(table_name, primary_keys: List[str]) -> str:
    keys_path = ','.join(['{' + pk.lower() + '}' for pk in primary_keys])
    return f"/{table_name.lower()}/{keys_path}"


def dim_soon(value):
    return f"[dim]{value} [white](soon!)[/white] [/dim]"


def dim(value):
    return f"[dim]{value}[/dim]"


def c(color, value):
    return f"[{color}]{value}[/{color}]"


class EndpointTableRenderer:

    def __init__(self, console):
        self.console = console
        self.table = self._table_header()

    @staticmethod
    def _table_header():
        table = Table(title=None, expand=False, show_edge=True, show_header=False, box=NONE_BOX)
        table.add_column("", style="magenta")
        table.add_column("", style="", overflow='fold')
        return table

    def newline(self):
        self.table.add_row("", "")

    def header(self, value):
        self.table.add_row("", f"[cyan]{value}[/cyan]")

    def simple_row(self, column):
        self.row("", column)

    def row(self, column_1, column_2, is_dimmed=False):
        if is_dimmed:
            self.table.add_row(dim_soon(column_1), dim(column_2))
        else:
            self.table.add_row(column_1, column_2)

    def render(self):
        self.console.print(self.table)


class EndpointRenderer:
    def __init__(self, patch_context, console: Console, source_state: StatePayload, name: str, output: str):
        self.patch_context = patch_context
        self.console = console
        self.source_state = source_state
        self.source_id = source_state.active_source_id
        self.name = name
        self.table = EndpointTableRenderer(self.console)
        self.output = output

    def render_base_url(self, suffix):
        return ''.join([self.patch_context.patch_endpoint, c('yellow', suffix)])

    def render_base_url_text(self, suffix):
        return ''.join([self.patch_context.patch_endpoint, suffix])

    def render_dataset_bases(self):
        self.table.row('GraphQL',
                       f"{self.render_base_url('/query/graphql')} (try [cyan]pat dataset playground {self.name}[/cyan])")
        self.table.row('REST', self.render_base_url('/query/rest/{route}'))

    def render_batch_bases(self):
        self.table.row('Batch', self.render_base_url('/batch/consume'))
        self.table.row('Batch Schema', self.render_base_url('/batch/schema.json'))

    def render_query_result(self, result: Optional[Dataset]):
        if self.output == 'table':
            self.render_query_result_table(result)
        if self.output == 'json':
            self.render_query_result_json(result)

    def render_query_result_json(self, result: Optional[Dataset]):
        if not result:
            self.console.print_json(None)
            return

        rest_routes = []
        for table in sorted(result.tables, key=lambda t: t.name):
            primary_key = [k.name for k in table.primaryKey]
            rest_routes.append({
                "method": "GET",
                "route": text_route(table.name, primary_key)
            })

        self.console.print_json(json.dumps({
            'dataset_id': result.id,
            'dataset_name': result.name,
            'endpoints': {
                'graphql': self.render_base_url_text('/query/graphql'),
                'rest': {
                    'base': self.render_base_url_text('/query/rest'),
                    'resources': rest_routes
                }
            }
        }))

    def render_query_result_table(self, result: Optional[Dataset]):
        has_batch = any(r.destination.type == "BATCH_API" for r in result.destinations)
        has_default = any(r.destination.type == "DATASET_API" for r in result.destinations)

        if result:
            self.table.header("Base URLs")
            if has_default:
                self.render_dataset_bases()
            if has_batch:
                self.render_batch_bases()
            if has_default and result.tables:
                self.table.newline()
                self.table.header("Routes")
                for result_table in result.tables:
                    primary_key = [k.name for k in result_table.primaryKey]
                    self.table.simple_row(table_route(result_table.name, primary_key))
                if has_curl():
                    self.table.newline()
                    self.table.header("Test it out")
                    self.table.simple_row(f"export BEARER_TOKEN=$(pat dataset bearer {self.name})")
                    curl = CurlRenderer()
                    limit = 10
                    for result_table in result.tables:
                        rendered_command = curl.render_url(self.render_base_url('/query/rest/' + result_table.name.lower()),
                                                           limit=limit)
                        self.table.simple_row(rendered_command)
                else:
                    self.table.newline()
                    self.table.header("No routes")
            self.table.render()
        else:
            self.console.print(f"Dataset {c('cyan', self.name)} "
                               f"for source ID {c('yellow', self.source_id)} has not been found.")
