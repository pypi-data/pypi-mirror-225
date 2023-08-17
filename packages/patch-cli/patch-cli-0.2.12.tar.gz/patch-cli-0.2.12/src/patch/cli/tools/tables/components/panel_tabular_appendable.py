from patch.cli.tools.tables.components.panel_tabular_positional_hierarchy import PanelTabularPositionalHierarchy


class PanelTabularAppendable(PanelTabularPositionalHierarchy):

    def remove_current_row(self):
        row = None
        if self.cursor.current_row is not None and self.cursor.current_row <= self.visible_rows_count() - 1:
            candidate = self.viewport.row_entry(self.cursor.current_row)
            if candidate:
                new_rows = []
                for r in self.rows:
                    if r == candidate:
                        row = candidate
                    else:
                        new_rows.append(r)
                if row is not None:
                    self.set_rows(new_rows)
        self.refresh()
        return row

    def append_row(self, row):
        self.rows.append(row)
        self.rows.sort(key=lambda r: r.id)
        self.refresh()
