from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List


@dataclass
class PanelTabularRow(ABC):

    @abstractmethod
    def check_visible(self) -> bool:
        pass

    @abstractmethod
    def set_visible(self, visible: bool) -> None:
        pass


@dataclass
class PanelTabularHierarchicalRow(PanelTabularRow):

    @abstractmethod
    def get_hierarchy(self) -> List[str]:
        pass
