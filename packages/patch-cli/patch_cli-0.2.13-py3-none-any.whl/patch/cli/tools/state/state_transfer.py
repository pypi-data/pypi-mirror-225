import requests


class StateTransfer:

    def __init__(self, patch_context, path):
        self.patch_context = patch_context
        self.path = path
        self._response = None

    def call_for_state_transfer(self, payload):
        headers = {"Content-Type": "application/json"}
        url = self.patch_context.patch_endpoint + self.path
        response = requests.get(url, params=payload, headers=headers, allow_redirects=True)
        response.raise_for_status()
        self._response = response.json()

    def get_redirect_url(self):
        if self._response:
            return self.patch_context.patch_endpoint + self._response.get('redirect-path')
