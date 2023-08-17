import dataclasses
from patch.cli.tools.tables.components.panel_tabular_positional_hierarchy import PanelTabularPositionalHierarchy


class PanelTabularPositional(PanelTabularPositionalHierarchy):

    def remove_current_row(self):
        row = None
        if self.cursor.current_row is not None and self.cursor.current_row <= self.visible_rows_count() - 1:
            candidate = self.viewport.row_entry(self.cursor.current_row)
            if candidate:
                candidate.is_visible = False
                row = dataclasses.replace(candidate, is_visible=True)
        if row and self.cursor.current_row == self.visible_rows_count() - 1:
            self.move_up()
        self.refresh()
        return row

    def append_row(self, row):
        for t in self.rows:
            if t.id == row.id:
                t.is_visible = True
                if not t.columns and row.columns:
                    t.columns = row.columns
                    t.row_count = row.row_count
                    t.size_bytes = row.size_bytes
                self.refresh()
