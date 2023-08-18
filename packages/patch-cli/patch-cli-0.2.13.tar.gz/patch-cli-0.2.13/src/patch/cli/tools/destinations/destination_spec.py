from typing import Dict, List
import json
from patch.cli.tools.config_spec import ConfigSpec
from patch.cli.tools.field_spec import FieldSpec, InputSpec, FieldSpecCondition, FieldChoice
from rich import box
from rich.table import Table

name_spec = FieldSpec(key="name", desc="Destination name", required=True)

conn_spec: Dict[str, InputSpec] = {
    'DATASET_API': InputSpec(
        name='DATASET_API',
        create_mutation_name='createDestination',
        fields=[]
    ),
    'BATCH_API': InputSpec(
        name='BATCH_API',
        create_mutation_name='createDestination', fields=[
            FieldSpec(key="retentionDays", desc="Retention days", required=False),
            # FieldSpec(key="maxBatchSize", desc="Maximum batch size", required=False),
        ]),
}

field_specs: List[FieldSpec] = [
    name_spec,
    FieldSpec(key="type", desc="Destination type", required=True, choices=[
        # FieldChoice(key='dataset', gql_value='DATASET_API'),
        FieldChoice(key='batch', gql_value='BATCH_API'),
    ], conditions=[
        # FieldSpecCondition(if_value='DATASET_API',
        #                    then_fields=conn_spec['DATASET_API'].fields),
        FieldSpecCondition(if_value='BATCH_API',
                           then_fields=conn_spec['BATCH_API'].fields),
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


class DestinationConfigSpec(ConfigSpec):

    def __init__(self, str_destination_type):
        super().__init__(conn_spec, name_spec, str_destination_type)
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
