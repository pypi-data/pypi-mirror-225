import sys

from cement import Controller, ex

from ..core.services import client


class Show(Controller):
    """
    Provides the `ursactl show ...` set of commands.
    """
    class Meta:
        label = 'show'
        stacked_on = 'base'
        stacked_type = 'nested'
        help = 'show something'

    @ex(help='show platform endpoint')
    def platform(self):
        print(self.app.config.get('ursactl', 'platform'))

    @ex(help='show default project')
    def project(self):
        print(self.app.config.get('ursactl', 'project'))

    @ex(help='show token')
    def token(self):
        iam_client = client('iam', self.app)
        token = iam_client.get_token()
        if token:
            print(token)
        else:
            sys.exit(1)
