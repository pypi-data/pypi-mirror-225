from cement import Controller, ex
import json
import yaml

from ..core.services import client


class Stop(Controller):
    """
    Provides the 'stop' verb.
    """

    class Meta:
        label = 'stop'
        stacked_on = 'base'
        stacked_type = 'nested'
        help = 'stop something'

    @ex(help='stop an agent',
        arguments=[
            (['id'], {'help': 'agent instance identifier', 'action': 'store'})
        ])
    def agent(self):
        planning_client = client('planning', self.app)
        result = planning_client.stop_agent(self.app.pargs.id)
        self._print(result)

    def _print(self, data):
        if self.app.pargs.output == 'json':
            print(json.dumps(data))
        else:
            print(yaml.dump(data))
