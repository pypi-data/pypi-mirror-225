from cement import Controller, ex

from ..core.services import client


class Refresh(Controller):
    """
    Provides the 'refresh' verb.
    """
    class Meta:
        label = 'refresh'
        stacked_on = 'base'
        stacked_type = 'nested'
        help = 'refresh something'

    @ex(help="refresh token")
    def token(self):
        iam_client = client('iam', self.app)
        iam_client.clear_token()
        iam_client.get_token()
