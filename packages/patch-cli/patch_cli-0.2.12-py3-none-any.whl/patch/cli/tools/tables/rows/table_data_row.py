from dataclasses import dataclass, field
from typing import List, Optional

from patch.cli.tools.tables.rows.panel_tabular_row import PanelTabularRow, PanelTabularHierarchicalRow


@dataclass
class ColumnsDataRow(PanelTabularRow):
    name: str
    type: str
    index: int
    selected: bool = False
    mutable: bool = True
    color: str = None

    def check_visible(self) -> bool:
        return True

    def set_visible(self, visible: bool) -> None:
        pass


@dataclass
class TableDataRow(PanelTabularHierarchicalRow):
    id: str
    database: str
    hierarchy: List[str]
    name: str
    type: str
    size_bytes: Optional[int]
    row_count: Optional[int]
    columns: List[ColumnsDataRow] = field(default_factory=list)
    is_visible: bool = True
    exists: bool = True

    def check_visible(self) -> bool:
        return self.is_visible

    def set_visible(self, visible: bool) -> None:
        self.is_visible = visible

    def set_columns(self, columns: List[ColumnsDataRow]):
        self.columns = columns

    def has_pk(self):
        return next((True for i in (self.columns or []) if i.selected), False)

    def get_hierarchy(self):
        return self.hierarchy


@dataclass
class TableDataRowWithPk(TableDataRow):
    pass
