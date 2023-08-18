from abc import ABC, abstractmethod
from typing import List, TypeVar, Generic

from rich.table import Table

from patch.cli.tools.tables.rows.panel_tabular_row import PanelTabularRow

RT = TypeVar("RT", bound=PanelTabularRow)


class RowCollection(ABC, Generic[RT]):

    @abstractmethod
    def get_rows(self) -> List[RT]:
        pass

    @abstractmethod
    def set_rows(self, rows: List[RT]) -> None:
        pass

    @abstractmethod
    def to_renderable_row(self, row: RT) -> List[str]:
        pass

    @abstractmethod
    def get_table_header(self) -> Table:
        pass
