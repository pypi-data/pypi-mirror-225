import os
import sys
from appdirs import user_data_dir
from pathlib import Path

from patch.storage.auth import AuthFileGeneric
from patch.storage.state_file import StateFile


def _require_patch_home(data_dir=None):
    migrate = False

    if data_dir is None:
        data_dir = os.environ.get('PATCH_HOME', None)

    if data_dir is None or data_dir == "":
        data_dir = user_data_dir(Storage.APPLICATION, Storage.VENDOR)
        migrate = True

    os.makedirs(data_dir, mode=0o770, exist_ok=True)

    deprecated_data_dir = os.path.join(Path.home(), Storage.DEPRECATED_PATCH_HOME)
    if migrate and os.path.isdir(deprecated_data_dir):
        print("Migrating user data from", deprecated_data_dir, "to", data_dir, file=sys.stderr)
        for file in ["auth.json", "source.json"]:
            path = os.path.join(deprecated_data_dir, file)
            if os.path.exists(path):
                os.rename(path, os.path.join(data_dir, file))
        os.rmdir(deprecated_data_dir)

    return data_dir


class Storage:
    VENDOR = "patch.tech"
    APPLICATION = "patch-cli"
    DEPRECATED_PATCH_HOME = ".patch-tech"

    def __init__(self, location=None):
        self._data_dir = _require_patch_home(location)
        self._auth_file = AuthFileGeneric(self._data_dir)
        self._state_file = StateFile(self._data_dir)

    @property
    def auth(self):
        return self._auth_file

    @property
    def source_state(self):
        return self._state_file
