from typing import List

from rich import box
from rich.table import Table


class RowRenderer:

    def __init__(self, record, title, color, count=None):
        self.record = record
        self.title = title
        self.color = color
        self.count = count
        self.column_set = set()
        self.value_map = {}
        self._build_value_map()

    @staticmethod
    def is_empty(record):
        return not RowRenderer._get_columns(record)

    @staticmethod
    def _get_columns(record):
        try:
            return record.columns
        except AttributeError:
            return []

    def _build_value_map(self):
        if self.record:
            columns = RowRenderer._get_columns(self.record)
            for column in columns:
                self.column_set.add(column.name)
                self.value_map[column.name] = column.value

    def render_title(self):
        if self.record:
            if self.count is not None:
                return f"{self.title} (count: {self.count})"
            else:
                return self.title
        else:
            return f"{self.title} [magenta](not found)[/magenta]"


class RowTableRenderer:

    def __init__(self, rows: List[RowRenderer]):
        self.rows = rows

    def _get_sorted_columns(self):
        columns = set()
        for row in self.rows:
            columns.update(row.column_set)
        return sorted(columns)

    def render_table(self, title):
        rendered_title = f"Table [yellow]{title}[/yellow]" if title is not None else ""
        inst = Table(title=rendered_title, show_edge=True, box=box.MINIMAL)
        inst.add_column("Column", justify="left", style="white", no_wrap=True)
        for row in self.rows:
            inst.add_column(row.render_title(), justify="left", style=row.color, no_wrap=True)
        for column in self._get_sorted_columns():
            column_values = []
            for row in self.rows:
                column_values.append(row.value_map.get(column, ""))
            inst.add_row(column, *column_values)
        return inst
