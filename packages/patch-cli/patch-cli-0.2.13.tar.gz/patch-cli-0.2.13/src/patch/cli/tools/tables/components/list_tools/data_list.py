from __future__ import annotations
from dataclasses import dataclass
from typing import List, Callable, TypeVar, Generic, Optional

from patch.cli.tools.tables.rows.panel_tabular_row import PanelTabularRow

RT = TypeVar("RT", bound=PanelTabularRow)


@dataclass
class FilteredEntry:
    value: RT


SubFilteredEntry = TypeVar("SubFilteredEntry", bound=FilteredEntry)


class DataList(Generic[SubFilteredEntry]):
    """
    A sequence of data rows.
    """
    filtered_entries: List[SubFilteredEntry]

    @classmethod
    def from_values(cls, values: Optional[List[RT]]):
        values = values or []
        filtered_entries = []
        for value in values:
            if value.check_visible():
                filtered_entries.append(FilteredEntry(value))
        return cls(filtered_entries)

    def __init__(self, filtered_entries):
        """
        Creates a new sequence of data rows from values.
        """
        self.filtered_entries = filtered_entries

    def size(self):
        return len(self.filtered_entries)

    def filter(self, fn: Callable[[SubFilteredEntry], bool]) -> DataList:
        """
        Filters data rows by a given predicate.
        """
        new_entries: List[SubFilteredEntry] = []
        idx = 0
        for entry in self.filtered_entries:
            if fn(entry):
                new_entries.append(entry)
                idx += 1
        return DataList(new_entries)

    def map(self, fn: Callable[[SubFilteredEntry], SubFilteredEntry]):
        """
        Maps rows.
        """
        new_entries = [fn(entry) for entry in self.filtered_entries]
        return DataList(new_entries)
