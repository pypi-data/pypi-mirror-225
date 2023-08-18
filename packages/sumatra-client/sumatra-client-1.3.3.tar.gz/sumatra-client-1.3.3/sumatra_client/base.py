from typing import Dict
import requests

class BaseClient:
    def __init__(self, client):
        self._gql_client = client

    def _execute_graphql(self, query: str, variables: Dict = None, headers: Dict = None, error_prefix: str = None) -> Dict:
        if variables is None:
            variables = {}
        if headers is None:
            headers = {}
        try:
            ret = self._gql_client.execute(query=query, variables=variables, headers=headers)
        except requests.exceptions.HTTPError as e:
            raise RuntimeError(f'HTTP error {e.response.status_code}: {e.response.text}')
        if "errors" in ret:
            msg = ret["errors"][0]["message"]
            if error_prefix is not None:
                msg = f'{error_prefix}: {msg}'
            raise RuntimeError(msg)
        return ret
