from dataclasses import dataclass
from typing import Any, List, Optional, Iterable


@dataclass
class FieldSpecCondition:
    if_value: str
    then_fields: List['FieldSpec']


@dataclass
class FieldChoice:
    gql_value: Any
    key: str


@dataclass
class FieldSpec:
    key: str
    desc: str
    required: bool
    is_password: bool = False
    type: str = "str"
    default: Any or List[Any] = None
    choices: Optional[List[FieldChoice]] = None
    conditions: Optional[List[FieldSpecCondition]] = None


def join_spec_keys(specs: Iterable[FieldSpec]) -> str:
    keys = [s.key for s in specs]
    return ", ".join(keys)


@dataclass
class InputSpec:
    fields: List[FieldSpec]
    name: str
    create_mutation_name: str
