from typing import TextIO, Optional

from patch.cli.tools.config import Config

from rich.prompt import Prompt

from patch.cli.tools.field_spec import FieldSpec
from patch.cli.tools.base64_encryption import b64_encryption


class ConfigInteractive(Config):

    def __init__(self, console, file_config: Optional[TextIO], staging_db: Optional[str] = None):
        super().__init__(file_config, staging_db)
        self.console = console

    def resolve_missing_config_field(self, field: FieldSpec):
        """Resolves the given field by prompting the user for a value."""
        choices = None
        if field.choices:
            choices = [ch.key for ch in field.choices]
            if not field.required:
                choices.append("")
        while True:
            value = Prompt.ask(field.desc, console=self.console, password=field.is_password, choices=choices)
            if value:
                if field.key == "credentialsKey":
                    return b64_encryption(value)
                else:
                    return value
            elif not field.required:
                return None
            self.console.print("[prompt.invalid]Value cannot be empty")

    def finalize_key_resolution(self) -> None:
        pass

    def finalize_key_resolution(self) -> None:
        pass

