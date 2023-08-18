from dataclasses import dataclass
from typing import TypeVar


@dataclass
class GenericPayload:
    pass


GP = TypeVar("GP", bound=GenericPayload)
