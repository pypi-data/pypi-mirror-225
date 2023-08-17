from rich.console import Console

from patch.gql.client import Client


class DatasetClient:

    def __init__(self, console: Console, gql_client: Client, source_id: str):
        self.console = console
        self.gql_client = gql_client
        self.source_id = source_id

    def query_dataset(self, name):
        gql_query = self.gql_client.prepare_query('datasetByName', input={
            'sourceId': self.source_id,
            'datasetName': name
        })
        with gql_query as q:
            q.__fields__('id', 'tables', 'versions', 'latestVersion')
        with self.console.status("[bold green]Checking dataset name...[/bold green]") as _status:
            return gql_query.execute()
