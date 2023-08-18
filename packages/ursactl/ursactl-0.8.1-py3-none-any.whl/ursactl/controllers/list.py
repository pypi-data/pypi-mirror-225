from cement import Controller, ex
from json import dumps as json_dump
from yaml import dump as yaml_dump
from configparser import NoOptionError

from ursactl.core.services import client
from ursactl.core.exc import UrsaProjectNotDefined


class List(Controller):
    """
    Provides the `ursactl list ...` actions.
    """

    class Meta:
        label = 'list'
        stacked_on = 'base'
        stacked_type = 'nested'
        help = 'list something'

    @ex(help='list agents',
        arguments=[
            (['--project'], {'help': 'project identifier', 'dest': 'project', 'action': 'store'}),
        ])
    def agents(self):
        planning_client = client('planning', self.app)

        agents = planning_client.list_agents(project_uuid=self._project_scope)
        if self.app.pargs.output is None:
            data = []
            for item in agents:
                data.append(
                    [item['name']]
                )
            data.sort()
            self.app.render(data, headers=['Name'])
        else:
            self._print(agents)

    @ex(help='list transforms',
        arguments=[
            (['--project'], {'help': 'project identifier', 'dest': 'project', 'action': 'store'}),
        ])
    def transforms(self):
        ape_client = client('ape', self.app)

        algos = ape_client.list_transforms(project_uuid=self._project_scope)

        if self.app.pargs.output is None:
            data = []
            for item in algos:
                data.append(
                    [item['path'], item['name'], item['type']]
                )
            data.sort()
            self.app.render(data, headers=['Path', 'Name', 'Type'])
        else:
            self._print(algos)

    @ex(help='list datasets',
        arguments=[
            (['--project'], {'help': 'project identifier', 'dest': 'project', 'action': 'store'}),
        ])
    def datasets(self):
        dss_client = client('dss', self.app)
        datasets = dss_client.list_datasets(self._project_scope)

        if self.app.pargs.output is None:
            data = []
            for item in datasets:
                data.append(
                    [item['path'], item['size'], item['content_type']]
                )
            data.sort()
            self.app.render(data, headers=['Path', 'Size', 'Type'])
        else:
            self._print(list(datasets))

    @ex(help='list pages',
        arguments=[
            (['--project'], {'help': 'project identifier', 'dest': 'project', 'action': 'store'}),
        ])
    def pages(self):
        page_client = client('page', self.app)

        pages = page_client.list_pages(project_uuid=self._project_scope)
        if self.app.pargs.output is None:
            data = []
            for item in pages:
                data.append(
                    [item['path'], item['title']]
                )
            data.sort()
            self.app.render(data, headers=['Path', 'Title'])
        else:
            self._print(pages)

    @ex(help='list generators',
        arguments=[
            (['--project'], {'help': 'project identifier', 'dest': 'project', 'action': 'store'}),
        ])
    def generators(self):
        ape_client = client('ape', self.app)

        generators = ape_client.list_generators(project_uuid=self._project_scope)
        if self.app.pargs.output is None:
            data = []
            for item in generators:
                data.append(
                    [
                        item['path'],
                        item['transform']['type'],
                        self._transform_name(item['transform'])
                    ]
                )
            data.sort()
            self.app.render(data, headers=['Path', 'Type', 'transform'])
        else:
            self._print(generators)

    @ex(help='list packages',
        arguments=[
            (['--project'], {'help': 'project identifier', 'dest': 'project', 'action': 'store'}),
        ])
    def packages(self):
        planning_client = client('planning', self.app)

        packages = planning_client.list_packages(project_uuid=self._project_scope)
        if self.app.pargs.output is None:
            data = []
            for item in packages:
                data.append(
                    [item['name']]
                )
            data.sort()
            self.app.render(data, headers=['Name'])
        else:
            self._print(packages)

    @ex(help='list pipelines',
        arguments=[
            (['--project'], {'help': 'project identifier', 'dest': 'project', 'action': 'store'}),
        ])
    def pipelines(self):
        ape_client = client('ape', self.app)

        if self.app.pargs.output is None:
            pipelines = ape_client.list_pipelines(project_uuid=self._project_scope)
            data = []
            for item in pipelines:
                data.append(
                    [item['path'], item['description']]
                )
            data.sort()
            self.app.render(data, headers=['Path', 'Description'])
        else:
            pipelines = ape_client.list_pipelines(
                project_uuid=self._project_scope,
                all=True)
            self._print(pipelines)

    @ex(help='list projects')
    def projects(self):
        projects_client = client('projects', self.app)
        projects = projects_client.list()

        if self.app.pargs.output is None:
            data = []
            for item in projects:
                data.append(
                    [item['name'], item['isArchived'], item['user']['handle'], item['description']])
            data.sort()
            self.app.render(data, headers=['Name', 'Archived?', 'Owner', 'Description'])
        else:
            self._print(list(projects))

    @ex(help='list running agents',
        arguments=[
            (['--project'], {'help': 'project identifier', 'dest': 'project', 'action': 'store'}),
            (['agent'], {'help': 'agent identifier', 'action': 'store', 'nargs': '?'})
        ])
    def running_agents(self):
        planning_client = client('planning', self.app)

        running_agents = planning_client.list_running_agents(agent_id=self.app.pargs.agent, project_uuid=self._project_scope)
        if self.app.pargs.output is None:
            data = []
            for item in running_agents:
                data.append(
                    [item['agent'], item['startedAt'], item['id'], item['status']]
                )
            data.sort()
            self.app.render(data, headers=['Agent', 'Started At', 'Instance UUID', 'Status'])
        else:
            self._print(running_agents)

    @ex(help='list pipeline runs',
        arguments=[
            (['--project'], {'help': 'project identifier', 'dest': 'project', 'action': 'store'}),
            (['pipeline'], {'help': 'pipeline identifier', 'action': 'store', 'nargs': '?'})
        ])
    def pipeline_runs(self):
        ape_client = client('ape', self.app)

        pipeline_runs = ape_client.list_pipeline_runs(pipeline_id=self.app.pargs.pipeline, project_uuid=self._project_scope)

        if self.app.pargs.output is None:
            data = []
            for item in pipeline_runs:
                data.append(
                    [item['pipeline'], item['jobStatus'], item['dataset']]
                )
            data.sort()
            self.app.render(data, headers=['Pipeline', 'Status', 'Dataset'])
        else:
            self._print(pipeline_runs)

    @property
    def _project_scope(self):
        try:
            scope = self.app.pargs.project or self.app.config.get('ursactl', 'project')
        except NoOptionError:
            raise UrsaProjectNotDefined("Project must be defined.")
        return scope

    def _print(self, data):
        if self.app.pargs.output == 'json':
            print(json_dump(data))
        else:
            print(yaml_dump(data))

    def _transform_name(self, transform):
        return f"{transform['project']['user']['handle']}/{transform['project']['name']}:{transform['path']}"
