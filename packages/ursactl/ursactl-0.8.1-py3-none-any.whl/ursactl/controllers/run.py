from cement import Controller, ex
import json
import yaml

from ..core.services import client


class Run(Controller):
    """
    Provides the 'run' verb.
    """

    class Meta:
        label = 'run'
        stacked_on = 'base'
        stacked_type = 'nested'
        help = 'run something'

    @ex(help='run agent',
        arguments=[
            (['--project'], {'help': 'project identifier', 'dest': 'project', 'action': 'store'}),
            (['agent'], {'help': 'agent uuid or path', 'action': 'store'})
        ])
    def agent(self):
        planning_client = client('planning', self.app)
        result = planning_client.run_agent(self.app.pargs.agent, project_uuid=self._project_scope)
        self._print(result)

    @ex(help='run pipeline',
        arguments=[
            (['--project'], {'help': 'project identifier', 'dest': 'project', 'action': 'store'}),
            (['--param'], {'help': 'pipeline parameter', 'dest': 'parameters', 'action': 'append'}),
            (['--sweep-param'], {'help': 'pipeline sweep parameter', 'dest': 'sweep_parameters', 'action': 'append'}),
            (['pipeline'], {'help': 'pipeline path', 'action': 'store'})
        ])
    def pipeline(self):
        ape_client = client('ape', self.app)
        pipeline = self.app.pargs.pipeline
        parameters = None
        sweep_parameters = None
        if self.app.pargs.parameters:
            parameters = {
                k: json.loads(v)
                for k, v in dict(item.split('=') for item in self.app.pargs.parameters).items()
            }
        if self.app.pargs.sweep_parameters:
            sweep_parameters = {
                k: json.loads(v)
                for k, v in dict(item.split('=') for item in self.app.pargs.sweep_parameters).items()
            }

        result = ape_client.run_pipeline(
            pipeline=pipeline,
            parameters=parameters,
            sweep_parameters=sweep_parameters,
            project=self._project_scope)
        self._print(result)

    def _print(self, data):
        if self.app.pargs.output == 'json':
            print(json.dumps(data))
        else:
            print(yaml.dump(data))

    @property
    def _project_scope(self):
        return self.app.pargs.project or self.app.config.get('ursactl', 'project')
