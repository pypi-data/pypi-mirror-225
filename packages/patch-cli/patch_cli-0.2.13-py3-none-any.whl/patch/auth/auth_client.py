import json
import urllib
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

import http.client, urllib.parse
from patch import constants
from patch.auth.auth_token import global_access_token
from requests import HTTPError


class AuthResponseStatus(Enum):
    Success = 'Success',
    Failure = 'Failure'
    Pending = 'Pending'


@dataclass
class AuthResponse:
    status: AuthResponseStatus = field(init=False)


@dataclass
class AuthResponseFailure(AuthResponse):
    error: str

    def __post_init__(self):
        self.status = AuthResponseStatus.Failure


@dataclass
class AuthResponsePendingVerification:
    to: str
    channel: str


@dataclass
class AuthResponsePending(AuthResponse):
    verification: AuthResponsePendingVerification

    def __post_init__(self):
        self.status = AuthResponseStatus.Pending


@dataclass
class AuthResponseSuccess(AuthResponse):
    token: str
    refresh_token: str

    def __post_init__(self):
        self.status = AuthResponseStatus.Success


class AuthClient:

    def __init__(self, patch_context):
        self._patch_context = patch_context

    def login_or_signup_phone(self, phone):
        try:
            body = self.call_post('/auth/login', authform=phone, selection="phone")
            status = body.get('result', None)
            if status == 'OK':
                return AuthResponsePending(verification=AuthResponsePendingVerification(to=phone, channel='sms'))
            else:
                return AuthResponseFailure(error=f"Error: Auth server returned status #{status}")
        except HTTPError as e:
            message = e.response.json().get('message', None) \
                      or f"Auth server responded with HTTP code {e.response.status_code}"
            return AuthResponseFailure(error=f"Error: {message}")

    def login_or_signup_email(self, email):
        try:
            body = self.call_post('/auth/login', authform=email, selection="email")
            status = body.get('result', None)
            if status == 'OK':
                return AuthResponsePending(verification=AuthResponsePendingVerification(to=email, channel='email'))
            else:
                return AuthResponseFailure(error=f"Error: Auth server returned status #{status}")
        except HTTPError as e:
            message = e.response.json().get('message', None) \
                      or f"Auth server responded with HTTP code {e.response.status_code}"
            return AuthResponseFailure(error=f"Error: {message}")

    def validate_phone(self, phone, code):
        try:
            body = self.call_post('/auth/login/verify/sms', phone=phone, code=code)
            token = body['token']
            refresh_token = body['refreshToken']
            return AuthResponseSuccess(token=token, refresh_token=refresh_token)
        except HTTPError as e:
            message = e.response.json().get('message', None) \
                      or f"Auth server responded with HTTP code {e.response.status_code}"
            return AuthResponseFailure(error=f"Error: {message}")

    def validate_email(self, email, code):
        try:
            body = self.call_post('/auth/login/verify/email', email=email, code=code)
            token = body['token']
            refresh_token = body['refreshToken']
            return AuthResponseSuccess(token=token, refresh_token=refresh_token)
        except HTTPError as e:
            message = e.response.json().get('message', None) \
                      or f"Auth server responded with HTTP code {e.response.status_code}"
            return AuthResponseFailure(error=f"Error: {message}")

    def call_refresh(self, current_refresh):
        try:
            return self.call_post('/auth/refresh', refreshToken=current_refresh)
        except HTTPError as e:
            message = e.response.json().get('message', None) \
                      or f"Auth server responded with HTTP code {e.response.status_code}"
            raise Exception(f"Error: {message}")

    def call_post(self, path, **kwargs):
        params = bytes(json.dumps(kwargs), 'utf-8')
        headers = {"Content-type": "application/json", "User-Agent": constants.USER_AGENT}
        req = urllib.request.Request(self._patch_context.patch_endpoint + "/v1" + path, data=params, headers=headers, method='POST')
        response = self._patch_context.urlopen(req)
        data = response.read()
        response.close()
        if response.status >= 400:
            raise Exception(f"Error: HTTP status {response.status}")
        return json.loads(data)

    def get_access_token(self) -> Optional[str]:
        if global_access_token and global_access_token.has_token():
            if global_access_token.needs_refresh():
                token_payload = self.call_refresh(global_access_token.get_refresh())
                new_access_token = token_payload['token']
                refresh_token = token_payload['refreshToken']
                global_access_token.store(new_access_token, refresh_token)
                return new_access_token
            else:
                return global_access_token.get_access_token()
