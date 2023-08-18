from typing import List

from rich import box
from rich.table import Table

from patch.cli.tools.tables.rows.table_data_row import ColumnsDataRow
from patch.cli.tools.tables.rows.row_collection import RowCollection


class ColumnsRowCollection(RowCollection[ColumnsDataRow]):
    rows: List[ColumnsDataRow]

    def __init__(self, rows: List[ColumnsDataRow]):
        self.set_rows(rows)

    def get_rows(self) -> List[ColumnsDataRow]:
        return self.rows

    def set_rows(self, rows: List[ColumnsDataRow]) -> None:
        self.rows = rows

    def to_renderable_row(self, row: ColumnsDataRow) -> List[str]:
        return [row.name, row.type, "YES" if row.selected else ""]

    def get_table_header(self) -> Table:
        table = Table(title=None, expand=True, box=box.MINIMAL)
        table.add_column("Name", style="magenta")
        table.add_column("Type", style="cyan")
        table.add_column("Primary Key?", style="cyan")
        return table
