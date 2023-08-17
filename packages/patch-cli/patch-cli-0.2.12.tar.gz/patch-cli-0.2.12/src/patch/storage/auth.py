from dataclasses import dataclass

from patch.storage.generic_payload import GenericPayload
from patch.storage.generic_storage_file import GenericStorageFile


@dataclass
class AuthPayload(GenericPayload):
    access_token: str
    refresh_token: str


class AuthFileGeneric(GenericStorageFile[AuthPayload]):
    def __init__(self, location):
        super().__init__(location, 'auth.json')
