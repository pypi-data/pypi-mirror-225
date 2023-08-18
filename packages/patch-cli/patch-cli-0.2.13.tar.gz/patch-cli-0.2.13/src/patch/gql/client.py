import os
from typing import Dict
from sgqlc.operation import Operation

from sgqlc.endpoint.http import HTTPEndpoint

from patch.auth.auth_client import AuthClient
from patch.debug import debug_log
from patch.gql.schema import Query, Mutation
from patch import constants


class GqlExecutionError(Exception):

    def __init__(self, errors):
        self.errors = errors
        messages = [e.get('message') for e in errors]
        super().__init__("\n".join(messages))


class GqlCallContextManager:

    def __init__(self, client: 'Client', op: Operation, query_name: str, variables):
        self._client = client
        self._op = op
        self._query_name = query_name
        self._variables = variables
        self._q = getattr(self._op, self._query_name)(**self._variables)

    def __enter__(self):
        return self._q

    def __exit__(self, exc_type, exc_val, exc_tb):
        return True

    def execute(self):
        result = self._client.execute(self._op)
        return getattr(result, self._query_name)


class Client:
    DEFAULT_TIMEOUT: int = 300  # 5 minutes

    def __init__(self, patch_context, as_tenant=None):
        self._gql_url = patch_context.patch_endpoint + "/graphql"
        self.auth_client = AuthClient(patch_context)
        self._as_tenant = as_tenant
        self._urlopen = patch_context.urlopen

    def execute(self, operation, variables=None):
        gql_result = self._call_operation(operation, variables)
        errors = gql_result.get('errors')
        if errors:
            self._debug_errors(errors, operation, variables)
            raise GqlExecutionError(errors)
        result = operation + gql_result
        return result

    def prepare_query(self, query_name: str, **kwargs):  # -> Generator[Operation, None, Operation]:
        op_q = Operation(Query)
        return GqlCallContextManager(self, op_q, query_name, kwargs)

    def prepare_mutation(self, query_name: str, **kwargs):  # -> Generator[Operation, None, Operation]:
        op_q = Operation(Mutation)
        return GqlCallContextManager(self, op_q, query_name, kwargs)

    def get_url(self):
        return self._gql_url

    def _debug_errors(self, errors, operation, variables):
        debug_log({
            "url": self._gql_url,
            "errors": errors,
            "operation": operation,
            "variables": variables
        })

    def _call_operation(self, operation, variables):
        if variables is None:
            variables = {}
        headers = self._add_auth_headers({
            "User-Agent": constants.USER_AGENT,
        })
        endpoint = HTTPEndpoint(self._gql_url, headers, timeout=Client.DEFAULT_TIMEOUT, urlopen=self._urlopen)
        return endpoint(operation, variables)

    def _add_auth_headers(self, headers=None) -> Dict[str, str]:
        if headers is None:
            headers = {}
        else:
            headers = {**headers}

        token = self.auth_client.get_access_token()
        if token:
            headers['Authorization'] = token
        if self._as_tenant:
            headers['X-Patch-TenantId'] = self._as_tenant
        return headers
