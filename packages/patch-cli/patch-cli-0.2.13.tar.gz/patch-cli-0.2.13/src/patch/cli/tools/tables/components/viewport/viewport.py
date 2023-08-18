from dataclasses import dataclass
from textual.widget import Widget

from patch.cli.tools.tables.components.list_tools.data_list import DataList, FilteredEntry


@dataclass
class ViewableEntry(FilteredEntry):
    """DataEntity class extended with visual aspects"""
    height: int


class ViewPort:
    """
    Viewport is a "visible window" with data.
    It maintains a list of rows that are actually visible on the widget area.
    """
    widget: Widget
    input_list: DataList
    viewable_list: DataList
    has_more: bool
    offset: int

    def __init__(self, widget: Widget):
        self.widget = widget
        self.input_list = DataList.from_values([])
        self.viewable_list = self.input_list
        self.has_more = False
        self.offset = 0

    def reset(self):
        """
        Resets the position of the viewport.
        Should be called if the content changes significantly
        so that maintaining the position makes no sense anymore.
        """
        self.has_more = False
        self.offset = 0

    def get_height(self):
        """This is the width of the visible area within the widget accounting for the space taken up by the help text"""
        # The number 6 is a number of container rows that are not lists
        return self.widget.size.height - 6

    def feed_input_list(self, input_list: DataList[ViewableEntry]):
        """
        This function filters a given data list by what is actually visible in the viewport.
        The result, self.viewable_list, contains only rows that are going to be rendered to the screen.
        """
        self.input_list = input_list
        consumed_height = 0
        self.has_more = False
        max_height = self.get_height()
        idx = 0

        def test_fn(elem: ViewableEntry) -> bool:
            """
            This is the inner function provided as an input to the data filter.
            :param elem: The data row
            :return: True if the row will be rendered to the screen.
            """
            nonlocal idx
            idx += 1
            if idx <= self.offset:
                return False
            nonlocal consumed_height
            consumed_height += elem.height
            within_limit = consumed_height <= max_height
            if not within_limit:
                self.has_more = True
            return within_limit

        new_list = input_list.filter(test_fn)
        self.viewable_list = new_list
        return self.viewable_list

    def visible_rows_count(self):
        """How many rows will be visible within this viewport"""
        return self.viewable_list.size()

    def row_entry(self, idx):
        """Returns the source data for a given index in this viewport."""
        try:
            if idx is not None:
                entry = self.viewable_list.filtered_entries[idx]
                return entry.value
            return None
        except IndexError:
            return None

    def port_down(self):
        """Moves the viewport down (the rendered list is scrolled up)"""
        if self.has_more:
            self.offset += 1
            self.widget.refresh()

    def port_up(self):
        """Moves the viewport up (the rendered list is scrolled down)"""
        if self.offset > 0:
            self.offset -= 1
            self.widget.refresh()
