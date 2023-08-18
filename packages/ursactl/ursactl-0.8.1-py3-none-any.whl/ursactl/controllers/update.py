import sys

from cement import Controller, ex
import json
import yaml

from ..core.services import client
from ursactl.controllers.utils.transforms import load_transform


def _yaml_load(fd):
    return list(yaml.load_all(fd, Loader=yaml.Loader))


class Update(Controller):
    '''
    Provides the 'update' verb.
    '''
    class Meta:
        label = 'update'
        stacked_on = 'base'
        stacked_type = 'nested'
        help = 'update something'

    @ex(help='update an existing project',
        arguments=[
            (['id'], {'help': 'project identifier', 'action': 'store'}),
            (['--name'], {'help': 'project name',
             'action': 'store', 'dest': 'name'}),
            (['--description'], {'help': 'project description',
             'action': 'store', 'dest': 'description'})
        ])
    def project(self):
        projects_client = client('projects', self.app)
        result = projects_client.update(
            id=self.app.pargs.id, name=self.app.pargs.name, description=self.app.pargs.description)
        self._print(result)

    @ex(help='update an existing transform',
        arguments=[
            (['file'], {'help': 'transform definition file', 'action': 'store'}),
            (['--project'], {'help': 'project identifier', 'dest': 'project', 'action': 'store'})
        ])
    def transform(self):
        project_uuid = self._project_scope
        ape_client = client('ape', self.app)

        file = self.app.pargs.file
        pages = load_transform(file)

        if pages is None:
            print(f"Unable to load transform from {file}")
            sys.exit(1)

        if not isinstance(pages, list):
            pages = [pages]

        for content in pages:
            args = {
                'path': content['path'],
                'type': content['type'],
                'name': content['name'],
                'implementation': content['implementation'],
                'configuration_schema': content['configurationSchema'],
                'project_uuid': project_uuid,
            }
            for key in ['description', 'inputs', 'outputs', 'tags']:
                if key in content:
                    args[key] = content[key]

            result = ape_client.update_transform(**args)
            self._print(result)

    @ex(help='update an existing generator from a file',
        arguments=[
            (['file'], {'help': 'generator definition file', 'action': 'store'}),
            (['--project'], {'help': 'project identifier', 'dest': 'project', 'action': 'store'}),
        ])
    def generator(self):
        ape_client = client('ape', self.app)

        file = self.app.pargs.file
        if file.endswith('.yaml') or file.endswith('.yml'):
            loader = _yaml_load
        elif file.endswith('.json'):
            loader = json.load
        else:
            print("Only YAML and JSON files may be uploaded.")
            sys.exit(1)

        with open(file, 'r', encoding='utf-8') as fd:
            pages = loader(fd)

        if not isinstance(pages, list):
            pages = [pages]

        for content in pages:
            args = {
                'path': content['path'],
                'transform': content['transform']['path'],
                'transform_configuration': content['transform']['configuration'],
                'load': content['load'],
                'project_uuid': self._project_scope
            }

            for key in ['extract', 'description', 'tags']:
                if key in content and content[key] is not None:
                    args[key] = content[key]

            result = ape_client.update_generator(**args)
            self._print(result)

    @ex(help='update an existing package from a file',
        arguments=[
            (['file'], {'help': 'package definition file', 'action': 'store'}),
            (['--project'], {'help': 'project identifier', 'dest': 'project', 'action': 'store'}),
        ])
    def package(self):
        project_uuid = self._project_scope
        planning_client = client('planning', self.app)

        file = self.app.pargs.file
        with open(file) as fd:
            # read the content of the file
            content = fd.read()

        result = planning_client.update_package(project_uuid=project_uuid, content=content)
        self._print(result)

    @ex(help='update an existing pipeline from a file',
        arguments=[
            (['file'], {'help': 'pipeline definition file', 'action': 'store'}),
            (['--project'], {'help': 'project identifier', 'dest': 'project', 'action': 'store'}),
        ])
    def pipeline(self):
        ape_client = client('ape', self.app)

        file = self.app.pargs.file
        if file.endswith('.yaml') or file.endswith('.yml'):
            loader = _yaml_load
        elif file.endswith('.json'):
            loader = json.load
        else:
            print("Only YAML and JSON files may be uploaded.")
            sys.exit(1)

        with open(file, 'r', encoding='utf-8') as fd:
            pages = loader(fd)

        if not isinstance(pages, list):
            pages = [pages]

        for content in pages:
            args = {
                'path': content['path'],
            }
            args['project_uuid'] = self._project_scope

            for key in ['seeders', 'generators', 'description', 'tags']:
                if key in content and content[key] is not None:
                    args[key] = content[key]

            result = ape_client.update_pipeline(**args)
            self._print(result)

    def _print(self, data):
        if self.app.pargs.output == 'json':
            print(json.dumps(data))
        else:
            print(yaml.dump(data))

    @property
    def _project_scope(self):
        return self.app.pargs.project or self.app.config.get('ursactl', 'project')
