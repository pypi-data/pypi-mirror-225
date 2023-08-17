from dataclasses import dataclass
from typing import List, Dict, Optional


@dataclass
class RowRenderer:
    change: List[str]
    hierarchy: List[str]


class HierarchyRenderer:

    def __init__(self, color, column_idx, rows):
        self.color = color
        self.column_idx = column_idx
        self.rows = rows
        self.row_info: Dict[str, Optional[RowRenderer]] = {}
        self._process_rows()

    def _process_rows(self):
        last_hierarchy = None
        for row in self.rows:
            new_hierarchy = row.get_hierarchy()
            change = self.hierarchy_level_changed(last_hierarchy, new_hierarchy)
            last_hierarchy = new_hierarchy
            self.row_info[row.id] = RowRenderer(change, hierarchy=new_hierarchy)

    def _c(self, value, repeat=1):
        return f"[{self.color}]{str(value) * repeat}[/{self.color}]"

    def _get_renderer(self, row):
        return self.row_info.get(row.id, [])

    def get_change(self, row):
        return self._get_renderer(row).change

    def render_table_row(self, row, table_row):
        renderer = self._get_renderer(row)
        h_len = len(renderer.hierarchy)
        if renderer:
            elem_to_change = table_row[self.column_idx]
            new_elem = self._c('│ ', h_len - 1) + self._c('├ ') + elem_to_change
            return table_row[0:self.column_idx] + [new_elem] + table_row[self.column_idx + 1:]
        else:
            return table_row

    def headers(self, row):
        renderer = self._get_renderer(row)
        if renderer and renderer.change:
            h_len = len(renderer.hierarchy)
            for idx, elem in enumerate(renderer.change):
                if elem:
                    row_str = []
                    if idx == 0:
                        row_str.append(self._c(elem))
                    elif idx >= 1:
                        row_str.append(self._c('│ ', idx - 2))
                        row_str.append(self._c('├ '))
                        row_str.append(self._c(elem))

                    hierarchy_elem = ''.join(row_str)
                    row = [''] * self.column_idx + [hierarchy_elem] + [''] * (h_len - 1 - self.column_idx)
                    yield row

    @staticmethod
    def hierarchy_level_changed(old_h, new_h):
        """Returns list of possible hierarchy elements to render"""
        if old_h is None:
            return new_h
        elif old_h == new_h:
            return []
        else:
            result = []
            for i in range(len(old_h)):
                if old_h[i] == new_h[i]:
                    result.append('')
                else:
                    result.append(new_h[i])
            return result
