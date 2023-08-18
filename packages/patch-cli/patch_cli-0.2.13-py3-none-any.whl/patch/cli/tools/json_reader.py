import json
from json import JSONDecodeError
from typing import Optional, TextIO, Type


def read_json(file: Optional[TextIO], error_class: Type[Exception]) -> dict:
    try:
        result = json.load(file) if file else {}
        if not isinstance(result, dict):
            raise error_class("File is not in valid JSON format")
        return result
    except (TypeError, JSONDecodeError):
        raise error_class("File is not in valid JSON format")
