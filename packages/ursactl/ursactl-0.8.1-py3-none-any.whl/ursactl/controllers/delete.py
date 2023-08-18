from cement import Controller, ex
import json
import yaml

from ..core.services import client


class Delete(Controller):
    """
    Provides the 'delete' verb.
    """

    class Meta:
        label = 'delete'
        stacked_on = 'base'
        stacked_type = 'nested'
        help = 'delete something'

    @ex(help='delete an agent',
        arguments=[
            (['--project'], {'help': 'project identifier', 'dest': 'project', 'action': 'store'}),
            (['agent'], {'help': 'agent uuid or path', 'action': 'store'})
        ])
    def agent(self):
        planning_client = client('planning', self.app)
        result = planning_client.delete_agent(self.app.pargs.agent, project_uuid=self._project_scope)
        self._print(result)

    @ex(help='delete a transform',
        arguments=[
            (['--project'], {'help': 'project identifier', 'dest': 'project', 'action': 'store'}),
            (['transform'], {'help': 'transform uuid or path', 'action': 'store'})
        ])
    def transform(self):
        ape_client = client('ape', self.app)

        result = ape_client.delete_transform(self.app.pargs.transform, project_uuid=self._project_scope)
        self._print(result)

    @ex(help='delete a dataset',
        arguments=[
            (['--project'], {'help': 'project identifier', 'dest': 'project', 'action': 'store'}),
            (['dataset_uuid'], {'help': 'The UUID of the dataset to delete'})
        ])
    def dataset(self):
        dss_client = client('dss', self.app)
        result = dss_client.delete_dataset(self.app.pargs.dataset_uuid, project_uuid=self._project_scope)
        self._print(result)

    @ex(help='delete a generator',
        arguments=[
            (['--project'], {'help': 'project identifier', 'dest': 'project', 'action': 'store'}),
            (['generator'], {'help': 'generator uuid or path', 'action': 'store'})
        ])
    def generator(self):
        ape_client = client('ape', self.app)

        result = ape_client.delete_generator(self.app.pargs.generator, project_uuid=self._project_scope)
        self._print(result)

    @ex(help='delete a package',
        arguments=[
            (['--project'], {'help': 'project identifier', 'dest': 'project', 'action': 'store'}),
            (['package'], {'help': 'package uuid or path', 'action': 'store'})
        ])
    def package(self):
        planning_client = client('planning', self.app)
        result = planning_client.delete_package(self.app.pargs.package, project_uuid=self._project_scope)
        self._print(result)

    @ex(help='delete pipeline',
        arguments=[
            (['--project'], {'help': 'project identifier', 'dest': 'project', 'action': 'store'}),
            (['pipeline'], {'help': 'pipeline uuid or path', 'action': 'store'})
        ])
    def pipeline(self):
        ape_client = client('ape', self.app)
        pipeline = self.app.pargs.pipeline
        result = ape_client.delete_pipeline(pipeline, project_uuid=self._project_scope)
        self._print(result)

    def _print(self, data):
        if self.app.pargs.output == 'json':
            print(json.dumps(data))
        else:
            print(yaml.dump(data))

    @property
    def _project_scope(self):
        return self.app.pargs.project or self.app.config.get('ursactl', 'project')
