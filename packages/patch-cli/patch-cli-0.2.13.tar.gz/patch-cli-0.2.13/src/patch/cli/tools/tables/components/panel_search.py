from textual.app import RenderResult
from textual.reactive import reactive
from textual.widgets import Label


class SearchContent(Label):
    mouse_over = reactive(False)
    search_text = reactive("")

    def render(self) -> RenderResult:
        return "[yellow]Search here >[yellow] " + self.search_text
