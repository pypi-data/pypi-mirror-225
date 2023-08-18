import json
import os
from dataclasses import asdict
from typing import Generic

from patch.debug import debug_log
from patch.storage.generic_payload import GP


class GenericStorageFile(Generic[GP]):

    def __init__(self, location, filename):
        self._filename = os.path.join(location, filename)

    def store(self, payload: GP):
        with open(self._filename, 'w') as f:
            json.dump(asdict(payload), f)

    def load(self) -> GP:
        with open(self._filename, 'r') as f:
            klass = self._payload_class()
            return klass(**json.load(f))

    def exists(self):
        return os.path.exists(self._filename) and os.path.isfile(self._filename)

    def delete(self):
        if self.exists():
            try:
                os.remove(self._filename)
            except OSError as error:
                debug_log({"error": error})

    def _payload_class(self):
        return self.__orig_bases__[0].__args__[0]
