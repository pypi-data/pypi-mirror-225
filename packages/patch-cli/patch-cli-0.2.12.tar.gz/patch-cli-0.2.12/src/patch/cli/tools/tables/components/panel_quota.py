import math

from textual.app import RenderResult
from textual.reactive import reactive
from textual.widgets import Static

from patch.cli.tools.tables.renders import render_number
from patch.cli.tools.tables.rows.table_row_collection_quota_aware import TableRowCollectionQuotaAware


def smart_round(value):
    rounded = round(value, 2)
    if rounded % 1 > 0:
        return rounded
    else:
        return math.floor(rounded)


def render_pct_color(pct):
    if pct > 1:
        return "red"
    elif pct > 0.8:
        return "yellow"
    else:
        return "default"


class PanelQuota(Static):
    mouse_over = reactive(False)
    quota: int = 0
    quota_used: int = 0
    staged_size = reactive(0)
    available_bytes: int = 0
    pct: float = 0.0
    pct_color: str = 'default'
    coll_quota_aware: TableRowCollectionQuotaAware

    def initialize(self, quota, quota_used, coll_quota_aware: TableRowCollectionQuotaAware):
        self.quota = quota
        self.quota_used = quota_used
        self.available_bytes = max(0, self.quota - self.quota_used)
        self.coll_quota_aware = coll_quota_aware

    def render(self) -> RenderResult:
        color = render_pct_color(self.pct)
        return f"[yellow]Available: [/yellow]{self.render_quota()}, " + \
               f"[yellow]Staged[/yellow]: [{color}]{self.render_staged()}[/{color}] " + \
               f"( [{color}]{self.pct:.2%}[/{color}] )"

    def render_quota(self):
        return render_number(self.available_bytes, 1024, ['', 'KB', 'MB', 'GB', 'TB'], smart_round)

    def render_staged(self):
        return render_number(self.staged_size, 1024, ['', 'KB', 'MB', 'GB', 'TB'], smart_round)

    def set_staged(self, staged_size):
        self.staged_size = staged_size or 0
        if self.available_bytes > 0:
            self.pct = self.staged_size / self.available_bytes
            self.pct_color = render_pct_color(self.pct)
            self.coll_quota_aware.update_space_left(self.available_bytes - self.staged_size)

    @property
    def submission_allowed(self) -> bool:
        return self.pct <= 1
