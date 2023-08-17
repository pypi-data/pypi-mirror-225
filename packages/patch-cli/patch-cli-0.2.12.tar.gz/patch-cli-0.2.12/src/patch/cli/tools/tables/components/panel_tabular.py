from typing import TypeVar, List

from rich.table import Table
from rich.text import Text
from textual.reactive import reactive
from textual.widget import Widget

from patch.cli.tools.tables.components.list_tools.data_list import DataList
from patch.cli.tools.tables.components.viewport.cursor_controller import RowChangedMessage, CursorController
from patch.cli.tools.tables.components.viewport.viewport import ViewPort, ViewableEntry
from patch.cli.tools.tables.rows.panel_tabular_row import PanelTabularRow
from patch.cli.tools.tables.rows.row_collection import RowCollection

RT = TypeVar("RT", bound=PanelTabularRow)


class PanelTabular(Widget):
    filter = reactive("")
    rows_collection = reactive(None)
    index = reactive(None)

    zero_text: str
    current_data_list: DataList = DataList.from_values([])
    viewport: ViewPort
    cursor: CursorController

    @classmethod
    def instance(cls, zero_text, rows_collection):
        panel = cls()
        panel.initialize(zero_text, rows_collection)
        panel.enable_messages(RowChangedMessage)
        return panel

    def initialize(self, zero_text, rows_collection: RowCollection):
        self.zero_text = zero_text
        self.rows_collection = rows_collection
        self.viewport = ViewPort(self)
        self.cursor = CursorController(self.viewport)

    @property
    def rows(self):
        return self.rows_collection.get_rows()

    def set_rows(self, rows: List[RT], should_reset_cursor=False):
        self.rows_collection.set_rows(rows)
        self.refresh()
        if should_reset_cursor:
            self.cursor.reset()

    def on_row_changed_message(self):
        self.current_row_changed()

    def get_table_header(self) -> Table:
        return self.rows_collection.get_table_header()

    def current_row_changed(self):
        pass

    def watch_filter(self, new_val):
        if new_val is not None:
            self.cursor.reset()

    def render(self):
        table = self.get_table_header()
        idx = 0
        viewable_list = self \
            .get_rows_to_render() \
            .map(lambda elem: ViewableEntry(elem.value, 1))
        data_list = self.viewport.feed_input_list(viewable_list)
        self.cursor.revalidate()

        for data_entry in data_list.filtered_entries:
            entry_value = data_entry.value
            rendered_row = self.rows_collection.to_renderable_row(entry_value)
            if rendered_row is not None:
                if entry_value.mutable:
                    style = "on blue"
                else:
                    style = "on grey69"
                style = style if self.cursor.has_control and idx == self.cursor.current_row else entry_value.color
                table.add_row(*[Text.from_markup(elem) for elem in rendered_row], style=style)
                idx += 1
        if idx == 0:
            return self.zero_text
        else:
            return table

    def get_rows_to_render(self) -> DataList:
        data_list = DataList.from_values(self.rows)
        if self.filter:
            data_list = data_list.filter(lambda entry: entry.value.name.upper().startswith(self.filter))
        return data_list

    def visible_rows_count(self):
        return len(self.viewport.viewable_list.filtered_entries)

    def has_visible_rows(self):
        return self.visible_rows_count() > 0

    def get_rows(self):
        return self.rows

    # === Control ===

    def can_have_control(self) -> bool:
        return self.has_visible_rows()

    def has_control(self):
        return self.cursor.has_control

    def gain_control(self):
        if self.can_have_control():
            self.cursor.gain_control()

    def release_control(self, fully=False):
        self.cursor.release_control(fully)

    def move_up(self) -> None:
        self.cursor.move_up()

    def move_down(self) -> None:
        self.cursor.move_down()
