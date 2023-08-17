from typing import Dict, List
import json
from patch.cli.tools.config_spec import ConfigSpec
from patch.cli.tools.field_spec import FieldSpec, InputSpec, FieldSpecCondition, FieldChoice
from rich import box
from rich.table import Table

name_spec = FieldSpec(key="name", desc="Source name", required=True)

conn_spec: Dict[str, InputSpec] = {
    'snowflake': InputSpec(
        name='Snowflake',
        create_mutation_name='sourceConnectSnowflake',
        fields=[
            FieldSpec(key="host", desc="Host", required=True),
            FieldSpec(key="warehouse", desc="Warehouse", required=True),
            FieldSpec(key="database", desc="Database", required=True),
            FieldSpec(key="schema", desc="Schema", required=True),
            FieldSpec(key="user", desc="User", required=True),
            FieldSpec(key="authenticationMethod", desc="Authentication Method", required=True,
                      default='password',
                      choices=[
                          FieldChoice(key='password', gql_value='PASSWORD'),
                          FieldChoice(key='rsa', gql_value='RSA'),
                      ], conditions=[
                    FieldSpecCondition(if_value='PASSWORD', then_fields=[
                        FieldSpec(key="password", desc="Password", required=True, is_password=True),
                    ])
                ]),
            FieldSpec(key="stagingDatabase", desc="Staging Database", required=False)]),
    'bigquery': InputSpec(
        name='BigQuery',
        create_mutation_name='sourceConnectBigQuery', fields=[
            FieldSpec(key="credentialsKey", desc="Path to BigQuery credentials file", required=True),
            FieldSpec(key="projectId", desc="Project ID", required=True),
            FieldSpec(key="location", desc="BigQuery location", required=False),
            FieldSpec(key="dataset", desc="BigQuery Dataset", required=False),
            FieldSpec(key="stagingProjectId", desc="Patch Staging Project", required=True)]),
    'azure-blob': InputSpec(
        name='Azure Blob Storage',
        create_mutation_name='sourceConnectAzureBlob', fields=[
            FieldSpec(key="containerName", desc="The name of the Blob Storage container", required=True),
            FieldSpec(key="accountName", desc="The name of the storage account that owns the container", required=True),
            FieldSpec(key="sasToken", desc="A SAS token which grants access to the container (or a directory within). Leave blank to use a Shared Key",
                      required=False,
                      conditions=[
                          FieldSpecCondition(if_value=None, then_fields=[
                             FieldSpec(key="sharedKey", desc="A Shared Key which grants access to the container", required=True)])])]),
    'databricks': InputSpec(
        name='Databricks',
        create_mutation_name='sourceConnectDatabricks', fields=[
            FieldSpec(key="hostname", desc="Hostname for your Databricks SQL endpoint", required=True),
            FieldSpec(key="httpPath", desc="httpPath for your Databricks SQL endpoint", required=True),
            FieldSpec(key="token", desc="Access token for your Databricks SQL endpoint", required=True)])
}

field_specs: List[FieldSpec] = [
    FieldSpec(key="name", desc="Source name", required=True),
    FieldSpec(key="type", desc="Connector type", required=True, choices=[
        FieldChoice(key='snowflake', gql_value='snowflake'),
        FieldChoice(key='bigquery', gql_value='bigquery'),
        FieldChoice(key='azure-blob', gql_value='azure-blob'),
        FieldChoice(key='databricks', gql_value='databricks'),
    ], conditions=[
        FieldSpecCondition(if_value='snowflake',
                           then_fields=conn_spec['snowflake'].fields),
        FieldSpecCondition(if_value='bigquery',
                           then_fields=conn_spec['bigquery'].fields),
        FieldSpecCondition(if_value='azure-blob',
                           then_fields=conn_spec['azure-blob'].fields),
        FieldSpecCondition(if_value='databricks',
                           then_fields=conn_spec['databricks'].fields),
    ])
]


def render_bool(value: bool):
    return "True" if value else "False"


def map_values(field: FieldSpec):
    result = {}
    if field.choices:
        for choice in field.choices:
            result[choice.gql_value] = choice.key
    return result


class ConnectorConfigSpec(ConfigSpec):

    def __init__(self, str_connector_type):
        super().__init__(conn_spec, name_spec, str_connector_type)
        largest_key = 0
        for line in self.get_spec_fields():
            if len(line.key) > largest_key:
                largest_key = len(line.key)
        self._largest_key = largest_key

    def render_line(self, table: Table, field: FieldSpec, required_desc: str, applicable_desc: str):
        table.add_row(field.key, field.desc, required_desc, applicable_desc)
        key_map = map_values(field)
        if field.conditions is not None:
            for condition in field.conditions:
                required = render_bool(field.required)
                expected_value = key_map.get(condition.if_value, condition.if_value)
                expected_value_as_json = json.dumps(expected_value)
                cond_applicable_desc = f"If field [cyan]{field.key}[/cyan] is [cyan]{expected_value_as_json}[/cyan]"
                for cond_field in condition.then_fields:
                    self.render_line(table, cond_field, required, cond_applicable_desc)

    def render_connector_spec(self):
        name = self.get_spec().name
        table = Table(title=name, box=box.SIMPLE, border_style="grey37", show_lines=False)
        table.add_column("Key", justify="right", style="cyan", min_width=self._largest_key)
        table.add_column("Description", justify="left", style="green", no_wrap=False)
        table.add_column("Required?", justify="left", style="green", no_wrap=True)
        table.add_column("Applicable?", justify="left", style="green", no_wrap=True)
        for line in self.get_spec_fields():
            self.render_line(table, line, render_bool(line.required), "Always")
        return table
