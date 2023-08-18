"""
Base class for API clients.
"""

import re
import requests

from python_graphql_client import GraphqlClient

from ursactl.core.exc import UrsaNotAuthorized


class Base:
    """
    Base class for clients.
    """
    def __init__(self, endpoint: str, app):
        from .. import services

        self.app = app
        self.endpoint = endpoint
        self.iam_client = services.client('iam', app)
        self.client = GraphqlClient(endpoint=f"{endpoint}api")

    def raw_query(self, query, variables={}, reauthorize=True):
        try:
            result = self.client.execute(query=query, variables=variables, headers={
                "authorization": f"Bearer {self.iam_client.get_token()}"
            })

            if 'errors' in result:
                for error in result['errors']:
                    if 'code' in error and error['code'] == 'Forbidden':
                        if reauthorize:
                            self.iam_client.clear_token()
                            return self.raw_query(query, variables, reauthorize=False)
                        raise UrsaNotAuthorized("Not authorized")
                    else:
                        print(error['message'])
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                if reauthorize:
                    self.iam_client.clear_token()
                    return self.raw_query(query, variables, reauthorize=False)
                raise UrsaNotAuthorized("Not authorized")
            else:
                raise e
        return result

    @staticmethod
    def is_uuid(s: str) -> bool:
        """
        Test if the string looks like a UUID.
        """
        if s is None:
            return False
        return re.match(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', s)
