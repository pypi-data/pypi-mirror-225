from typing import Optional, List, Dict

from patch.cli.tools.field_spec import FieldSpec, InputSpec


class ConfigSpecError(Exception):
    pass


class ConfigSpec:
    _spec: Dict[str, InputSpec]
    _name_spec: Dict[str, FieldSpec]
    _type: Optional[str]

    def __init__(self, spec, name_spec, str_type):
        self._spec = spec
        self._name_spec = name_spec
        self.set_type_from_str(str_type)
        pass

    @property
    def type(self):
        return self._type

    def set_type_from_str(self, str_type: Optional[str]) -> None:
        self._type = None
        if str_type:
            if str_type in self._spec.keys():
                self._type = str_type
            else:
                raise ConfigSpecError("Unknown type")

    def get_spec(self) -> Optional[InputSpec]:
        return self._spec[self._type]

    def get_spec_fields(self) -> List[FieldSpec]:
        return self.get_spec().fields

    @property
    def mutation_name(self):
        return self._spec[self._type].create_mutation_name

    def get_spec_fields_plus_name(self) -> List[FieldSpec]:
        new_spec = [self._name_spec]
        new_spec.extend(self.get_spec_fields())
        return new_spec
