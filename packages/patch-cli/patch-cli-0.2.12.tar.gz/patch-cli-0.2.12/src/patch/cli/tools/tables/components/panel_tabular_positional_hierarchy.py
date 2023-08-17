from rich.text import Text

from patch.cli.tools.tables.components.hierarchy_renderer import HierarchyRenderer
from patch.cli.tools.tables.components.list_tools.data_list import SubFilteredEntry
from patch.cli.tools.tables.components.panel_tabular import PanelTabular
from patch.cli.tools.tables.components.viewport.viewport import ViewableEntry


class PanelTabularPositionalHierarchy(PanelTabular):

    def render(self):
        table = self.get_table_header()
        idx = 0
        data_list = self.get_rows_to_render()
        rows = [entry.value for entry in data_list.filtered_entries]
        hr = HierarchyRenderer("magenta", 0, rows)

        def map_to_viewable(elem: SubFilteredEntry) -> ViewableEntry:
            headers = [h for h in hr.headers(elem.value)]
            return ViewableEntry(elem.value, len(headers) + 1)

        viewable_list = data_list.map(map_to_viewable)
        data_list = self.viewport.feed_input_list(viewable_list)
        self.cursor.revalidate()

        for entry in data_list.filtered_entries:
            row = entry.value
            table_row = self.rows_collection.to_renderable_row(row)
            for header_row in hr.headers(row):
                rendered_header = [Text.from_markup(elem) for elem in header_row]
                table.add_row(*rendered_header, style="")

            style = "on blue" if self.cursor.has_control and idx == self.cursor.current_row else None
            rendered_row = [Text.from_markup(elem) for elem in hr.render_table_row(row, table_row)]
            table.add_row(*rendered_row, style=style)
            idx += 1
        if idx == 0:
            return self.zero_text
        else:
            return table
