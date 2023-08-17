from rich.panel import Panel

from textual.app import ComposeResult, RenderResult
from textual.containers import Container

from textual.widgets import Static


class Header(Static):

    def __init__(self, *args, **kwargs):
        self.title = kwargs.pop('title', None)
        self.size_source = kwargs.pop('size_source', None)
        super().__init__(*args, **kwargs)

    def compute_height(self):
        return self.size_source.container_size.height

    def render(self) -> RenderResult:
        self.log(self.container_size.height)
        return Panel("", title=self.title, height=self.compute_height())


class ContainerPanel(Container):

    def __init__(self, *args, **kwargs):
        self.title = kwargs.pop('title', None)
        self.widgets = args
        super().__init__(**kwargs)

    def compose(self) -> ComposeResult:
        print(f"ContainerPanel {self.container_size}")
        yield Header(title=self.title, size_source=self)
        for widget in self.widgets:
            widget.add_class("inner-component")
            yield widget
