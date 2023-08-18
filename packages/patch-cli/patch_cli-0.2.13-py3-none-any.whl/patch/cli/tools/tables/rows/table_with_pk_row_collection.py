from typing import List

from rich import box
from rich.emoji import EMOJI
from rich.table import Table

from patch.cli.tools.tables.rows.table_data_row import TableDataRowWithPk
from patch.cli.tools.tables.renders import render_number
from patch.cli.tools.tables.rows.row_collection import RowCollection


class TableWithPkRowCollection(RowCollection[TableDataRowWithPk]):
    rows: List[TableDataRowWithPk]

    def __init__(self, rows: List[TableDataRowWithPk]):
        self.set_rows(rows)

    def get_rows(self) -> List[TableDataRowWithPk]:
        return self.rows

    def set_rows(self, rows: List[TableDataRowWithPk]) -> None:
        self.rows = rows

    def to_renderable_row(self, row: TableDataRowWithPk) -> List[str]:
        size_bytes = render_number(row.size_bytes or 0, 1024, ['B', 'KB', 'MB', 'GB', 'TB'])
        row_count = render_number(row.row_count or 0, 1000, ['', 'K', 'M', 'Bn'])
        row_rendered = row.name
        if row.has_pk():
            row_rendered = f"[green]{row.name} {EMOJI['white_check_mark']}[/green]"
        return [row_rendered, size_bytes, row_count]

    def get_table_header(self) -> Table:
        table = Table(title=None, expand=True, box=box.MINIMAL)
        table.add_column("Name", style="cyan")
        table.add_column("Size", style="cyan")
        table.add_column("Rows", style="cyan")
        return table
