import time

import requests
from requests import HTTPError

from patch.cli.tools.state.state_transfer import StateTransfer


class BiDirectionalStateTransfer(StateTransfer):

    def __init__(self, patch_context, path, path_poll):
        super().__init__(patch_context, path)
        self.path_poll = path_poll

    def get_poll_token(self):
        if self._response:
            return self._response.get('poll-token')

    def call_poll_token(self):
        headers = {"Content-Type": "application/json"}
        url = self.patch_context.patch_endpoint + self.path_poll + "/" + self.get_poll_token()
        response = requests.get(url, headers=headers, allow_redirects=True)
        try:
            response.raise_for_status()
        except HTTPError as e:
            if e.response.status_code == 404:
                return None
            else:
                raise e
        return response.json()

    def poll_for_state(self, timeout_minutes=5, pace_s=1):
        timeout_seconds = 6 * timeout_minutes
        t_start = time.time()
        while time.time() - t_start < timeout_seconds:
            time.sleep(pace_s)
            result = self.call_poll_token()
            if result:
                return result.get('state')
        raise TimeoutError("Poll timeout")
