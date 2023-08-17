from dataclasses import dataclass

from patch.storage.generic_payload import GenericPayload
from patch.storage.generic_storage_file import GenericStorageFile


@dataclass
class StatePayload(GenericPayload):
    active_source_name: str
    active_source_id: str


class StateFile(GenericStorageFile[StatePayload]):
    def __init__(self, location):
        super().__init__(location, 'source.json')
