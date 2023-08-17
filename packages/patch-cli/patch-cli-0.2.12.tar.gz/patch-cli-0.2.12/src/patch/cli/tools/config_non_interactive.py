from typing import Optional, TextIO, List

from patch.cli.tools.config import Config, SpecVerificationError
from patch.cli.tools.field_spec import FieldSpec


class ConfigNonInteractive(Config):
    missing_fields: List[FieldSpec]

    def __init__(self, file_config: Optional[TextIO], staging_db: Optional[str] = None):
        super().__init__(file_config, staging_db)
        self.missing_fields = []

    def resolve_missing_config_field(self, field: FieldSpec):
        if field.required:
            if field.default is not None:
                return field.default
            self.missing_fields.append(field)
        return None

    def finalize_key_resolution(self):
        if self.missing_fields:
            missing_field_names = [f.key for f in self.missing_fields]
            if len(self.missing_fields) == 1:
                raise SpecVerificationError(f"[red]Missing field: {missing_field_names[0]} [/red]")
            else:
                raise SpecVerificationError(f"[red]Missing fields: {', '.join(missing_field_names)} [/red]")
