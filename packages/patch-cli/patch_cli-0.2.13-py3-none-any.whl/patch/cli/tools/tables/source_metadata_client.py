import os
from rich.console import Console
from rich.prompt import Confirm
from rich.table import Table

from patch.cli.styled import NONE_BOX
from patch.cli.tools.tables.rows.table_data_row import TableDataRow, ColumnsDataRow
from patch.cli.tools.tables.source_data import SourceData
from patch.gql.client import Client
from patch.storage.state_file import StatePayload

default_ingest_mode = os.environ.get('PATCH_TABLE_INGEST_MODE', 'CONTINUOUS')


def get_hierarchy(table_id):
    segments = table_id.split('.')
    if len(segments) > 3:
        name = '.'.join(segments[2:])
        hierarchy = segments[0:2]
    else:
        name = segments[-1]
        hierarchy = segments[0:-1]
    return [name, hierarchy]


class SourceMetadataClient:

    def __init__(self, console: Console, gql_client: Client, state: StatePayload):
        self.console = console
        self.client = gql_client
        self.source_id = state.active_source_id
        self.source_name = state.active_source_name

    def query_source_description(self):
        gql_query = self.client.prepare_query('getSourceDescription', id=self.source_id)
        with gql_query as q:
            q.tables.__fields__()
            q.__fields__('quota', 'quotaUsed', 'id')
        with self.console.status("[bold green]Loading source structure...[/bold green]") as _status:
            return gql_query.execute()

    def format_dataset(self, dataset):
        dataset_data = {
            table['qualifiedTableIdentifier']: {
                'columns': {column["name"]: column["graphqlType"].upper() for column in table['columns']},
                'primaryKeys': [pk['name'] for pk in table['primaryKey']]
            } for table in dataset['tables']
        }
        return dataset_data
    
    def create_columns_data_row(self, c, table_data=None):
        column = table_data["columns"].get(c.name, None) if table_data else None
        color = None if column else 'bright_green'
        gqlType = c.graphqlType.upper() if not column or column == c.graphqlType.upper() else f'[bright_green]{c.graphqlType.upper()}[/bright_green]'
        selected = c.name in table_data["primaryKeys"] if table_data else False
        mutable = not table_data
        return ColumnsDataRow(name=c.name, type=gqlType, index=c.index, selected=selected, mutable=mutable, color=color)

    def get_source_metadata(self, dataset=None) -> SourceData:
        source_description = self.query_source_description()
        sorted_tables = sorted(source_description.tables, key=lambda tab: tab.id)
        dataset_data = self.format_dataset(dataset) if dataset else {}
        tables = []
        selected_tables = []
        obsolete_tables = []
        for t in sorted_tables:
            [name, hierarchy] = get_hierarchy(t.id)
            table_data = dataset_data.pop(t.id, None)
            columns = []
            # If a source table is part of this dataset, columns to display are  columns are the union of
            # those currently in the source and those in the current version of the dataset.
            if table_data:
                for c in t.columns:
                    columns.append(self.create_columns_data_row(c, table_data))
                    table_data['columns'].pop(c.name, None)
                remaining_columns = [(index, column_name, column_type) for index, (column_name, column_type) in enumerate(table_data['columns'].items())]
                columns += [ColumnsDataRow(name=column_name, type=column_type, index=index, selected=False, mutable=False, color='bright_red') for index, column_name, column_type in remaining_columns]
            # If a source table is not yet part of this dataset (or the dataset is being created now), all its
            # columns are available for selection
            else:
                columns = [ColumnsDataRow(name=c.name, type=c.graphqlType.upper(), index=c.index, selected=False, mutable=True) for c in t.columns if c.graphqlType]
            sorted_columns = sorted(columns, key=lambda col: col.index)
            table = TableDataRow(
                id=t.id, database=t.database, name=name, type=t.type, columns=sorted_columns, hierarchy=hierarchy,
                size_bytes=t.sizeBytes, row_count=t.rowCount)
            (selected_tables if table_data else tables).append(table)

        # Because of the `pop` above, dataset_data now contains only tables that are
        # in the dataset but no longer in the source.
        for table_id in dataset_data:
            table_data = dataset_data.get(table_id, None)
            [name, hierarchy] = get_hierarchy(table_id)
            columns = []
            for index, column_name in enumerate(table_data['columns']):
                column = ColumnsDataRow(name=column_name, type=table_data['columns'][column_name], index=index, selected=False, mutable=False, color='bright_red')
                columns.append(column)
            sorted_columns = sorted(columns, key=lambda col: col.index)
            table = TableDataRow(
                id=table_id, database=None, name=f'[bright_red]{name}[/bright_red]', type=None, columns=sorted_columns, hierarchy=hierarchy,
                size_bytes=0, row_count=0, exists = False)
            obsolete_tables.append(table)

        return SourceData(
            tables=tables,
            selected_tables=selected_tables,
            obsolete_tables=obsolete_tables,
            is_ready=False,
            quota=source_description.quota or 0,
            quota_used=source_description.quotaUsed or 0,
            source_id=source_description.id
        )

    def confirm_dataset(self, dataset_name, tables):
        self.console.print(f"\nYou are creating a dataset [cyan]{dataset_name}[/cyan] "
                           f"in the source [cyan]{self.source_name}[/cyan] "
                           f"(Source ID: [yellow]{self.source_id}[/yellow])")

        rt = Table(title=None, show_edge=True, box=NONE_BOX)
        rt.add_column("Location", justify="left", style="magenta", no_wrap=True)
        rt.add_column("Name", justify="left", style="cyan", no_wrap=True)
        rt.add_column("Primary key", justify="left", no_wrap=True)
        for table in tables:
            h = " . ".join(table.hierarchy)
            pk = []
            for column in table.columns:
                if column.selected:
                    pk.append(column.name)

            rt.add_row(h, table.name, ", ".join(pk))
        self.console.print(rt)
        return Confirm.ask("Proceed? ", console=self.console)

    def build_create_dataset_input(self, dataset_name, tables):
        tables_input = []
        for table in tables:
            columns_input = []
            for column in table.columns:
                if column.selected is True:
                    columns_input.append({'columnName': column.name})
            tables_input.append({
                'tableId': table.id,
                'primaryKey': columns_input,
                'ingestMode': default_ingest_mode
            })
        return {
            'sourceId': self.source_id,
            'datasetName': dataset_name,
            'tables': tables_input
        }
    
    def build_update_dataset_input(self, version, dataset_name, tables):
        tables_input = []
        for table in tables:
            columns_input = []
            for column in table.columns:
                if column.selected is True:
                    columns_input.append({'columnName': column.name})
            tables_input.append({
                'tableId': table.id,
                'ingestMode': default_ingest_mode,
                'primaryKey': columns_input
            })
        return {
            'sourceId': self.source_id,
            'datasetName': dataset_name,
            'tables': tables_input,
            'version': (version + 1)
        }
