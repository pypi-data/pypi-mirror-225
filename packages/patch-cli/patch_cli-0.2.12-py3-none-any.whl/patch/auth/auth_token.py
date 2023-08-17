from typing import Optional, List

import jwt
from jwt.exceptions import ExpiredSignatureError

from patch.storage.auth import AuthPayload
from patch.storage.storage import Storage


class AuthToken:

    def __init__(self):
        self.stored_auth = None
        self.storage = Storage()
        if self.storage.auth and self.storage.auth.exists():
            self.stored_auth = self.storage.auth.load()

    def needs_refresh(self) -> bool:
        try:
            if self.has_token():
                options = {'verify_signature': False, 'verify_exp': True}
                jwt.api_jwt.decode_complete(self.get_access_token(), options=options)
            return False
        except ExpiredSignatureError:
            return True

    def get_access_token(self) -> Optional[str]:
        if self.stored_auth:
            return self.stored_auth.access_token

    def get_refresh(self) -> Optional[str]:
        return self.stored_auth.refresh_token if self.stored_auth else None

    def has_token(self) -> bool:
        return self.get_access_token() is not None

    def store(self, new_access_token, new_refresh):
        self.storage.auth.store(AuthPayload(access_token=new_access_token, refresh_token=new_refresh))

    def delete(self):
        self.storage.auth.delete()

    def get_roles(self) -> List[any]:
        if self.has_token():
            options = {'verify_signature': False, 'verify_exp': False}
            jwt_payload = jwt.api_jwt.decode_complete(self.get_access_token(), options=options)
            return jwt_payload.get('payload', {}).get('patch.tech/graphql', {}).get('roles', [])
        return []


global_access_token = AuthToken()
global_token_roles = global_access_token.get_roles()
global_is_admin = 'admin' in global_token_roles
global_is_admin_or_mta = global_is_admin or ('multi-tenant' in global_token_roles)
