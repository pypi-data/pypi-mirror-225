

class SourceClient:

    def __init__(self, gql_client):
        self.gql_client = gql_client

    def get_sources_by_name(self, name):
        query = self.gql_client.prepare_query('getSourceList', input={'sourceName': name})
        return query.execute()

    def get_sources(self):
        query = self.gql_client.prepare_query('getSourceList', input={})
        return query.execute()

    def check_source_connectable(self, name):
        q = self.gql_client.prepare_query('getSourceStatus', input={'name': name})
        q.execute()
