from typing import Optional

from rich.align import Align
from rich.columns import Columns
from rich.console import Group
from rich.text import Text
from textual.app import RenderResult

from textual.reactive import reactive
from textual.widgets import Static

from patch.cli.tools.tables.components.panel_quota import PanelQuota


class PanelSummary(Static):
    mouse_over = reactive(False)
    selected_count = reactive(0)
    selected_ready = reactive(0)
    panel_quota: Optional[PanelQuota] = None

    def initialize(self, panel_quota):
        self.panel_quota = panel_quota

    def render(self) -> RenderResult:
        columns = [
            Align.left(Text.from_markup(
                f"[yellow]Selected: [/yellow]{self.selected_count}, " +
                f"[yellow]Ready:[/yellow] {self.selected_ready}"))]
        if self.panel_quota and not self.panel_quota.submission_allowed:
            columns.append(Align.right(Text.from_markup("[red]Quota exceeded![/red]")))
        elif self.is_all_set:
            columns.append(Align.right(
                Text.from_markup("[green]All set![/green] Press [yellow]ctrl+s[/yellow] to finish")))
        return Group(Columns(columns, expand=True))

    def set_selected(self, count, ready):
        self.selected_count = count
        self.selected_ready = ready

    @property
    def is_all_set(self) -> bool:
        return self.selected_count == self.selected_ready and self.selected_count > 0
