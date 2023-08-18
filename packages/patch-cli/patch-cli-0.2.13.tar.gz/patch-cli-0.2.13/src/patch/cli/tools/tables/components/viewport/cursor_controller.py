import asyncio
from typing import Optional

from textual.widget import Widget
from textual.message import Message, MessageTarget

from patch.cli.tools.tables.components.viewport.viewport import ViewPort


class RowChangedMessage(Message):

    def __init__(self, sender: MessageTarget) -> None:
        super().__init__(sender)


class CursorController:
    """Cursor Controller manages the position of the cursor within a given ViewPort."""
    has_control: bool
    current_row = Optional[int]
    remembered_row: int
    viewport: ViewPort
    widget: Widget

    def __init__(self, viewport: ViewPort):
        self.viewport = viewport
        self.has_control = False
        self.widget = viewport.widget
        self.reset()
        super().__init__()

    def reset(self):
        """Resets the position of the cursor back to the top."""
        self.viewport.reset()
        self.current_row = None
        self.remembered_row = 0

    def revalidate(self):
        """
        When data changes (e.g., rows were removed) the cursor may find itself out of the visible boundaries.
        This function corrects the cursor position back to the visible area.
        """
        rows_count = self.viewport.visible_rows_count()
        if self.has_control and self.current_row is None:
            self.current_row = 0
        if self.current_row is not None and self.current_row >= rows_count:
            self.move_up()

    def _set_current_row(self, value):
        """
        Sets the cursor fo a given position.
        Sends a message to the base widget.
        """
        self.current_row = value
        if value is not None:
            self.remembered_row = value
        message = RowChangedMessage(self.widget)
        asyncio.get_event_loop().create_task(self.widget.post_message(message))
        self.widget.refresh()

    def gain_control(self):
        """
        Called when the underlying widget gets focus, and key types start affecting this cursor.
        As the effect, rendered list will highlight the current cursor position.
        """
        if self.current_row is None:
            self._set_current_row(self.remembered_row)
        self.has_control = True
        self.widget.current_row_changed()
        self.widget.refresh()

    def release_control(self, fully=False):
        """
        The cursor loses focus.
        :param fully: If True, the cursor position is reset to the first row.
        """
        if self.has_control:
            self.has_control = False
            self._set_current_row(None)
            if fully:
                self.remembered_row = 0
            self.widget.refresh()

    def _cursor_position_down(self):
        """
        Low level function that moves the position of the cursor to one position down without affecting the viewport.
        """
        rows_count = self.viewport.visible_rows_count()
        if self.current_row < rows_count - 1:
            self._set_current_row(self.current_row + 1)

    def _cursor_position_up(self):
        """
        Low level function that moves the position of the cursor to one position up without affecting the viewport.
        """
        if self.current_row > 0:
            self._set_current_row(max(0, self.current_row - 1))

    def move_up(self) -> None:
        """
        Moves cursor to the previous element on the list.
        It either moves the viewport or just moves the position of the cursor.
        """
        if self.current_row is not None:
            first_visible = self.viewport.offset == 0
            last_visible = not self.viewport.has_more
            if first_visible:
                self._cursor_position_up()
            elif last_visible:
                if self.current_row <= (self.viewport.get_height() - 2) / 2:
                    self.viewport.port_up()
                else:
                    self._cursor_position_up()
            else:
                self.viewport.port_up()

    def move_down(self) -> None:
        """
        Moves cursor to the next element on the list.
        It either moves the viewport or just moves the position of the cursor.
        """
        rows_count = self.viewport.visible_rows_count()
        if rows_count == 0:
            return
        first_visible = self.viewport.offset == 0
        last_visible = not self.viewport.has_more
        if first_visible and last_visible:
            self._cursor_position_down()
        elif first_visible:
            if self.current_row >= (self.viewport.get_height() - 2) / 2:
                self.viewport.port_down()
            else:
                self._cursor_position_down()
        elif last_visible:
            self._cursor_position_down()
        else:
            self.viewport.port_down()
