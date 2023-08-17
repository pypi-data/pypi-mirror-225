from contextlib import contextmanager
from typing import Generator, Any

from patch.cli.tools.tables.components.panel_tabular import PanelTabular


class PanelTabularAllIn(PanelTabular):

    def replace_rows(self, rows):
        self.set_rows(rows, should_reset_cursor=True)
        self.refresh()

    @contextmanager
    def modify_current_row(self) -> Generator[Any, None, None]:
        yield self.viewport.row_entry(self.cursor.current_row)
        self.refresh()
