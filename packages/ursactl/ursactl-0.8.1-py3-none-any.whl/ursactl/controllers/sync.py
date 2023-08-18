from pathlib import Path
import re
import sys

from cement import Controller
import json
import yaml

from ..core.services import client
from ..core.utils.magic import magic
import ursactl.controllers.utils.transforms
import ursactl.controllers.utils.pages


class Sync(Controller):
    """
    Provides the 'sync' verb
    """

    class Meta:
        label = 'sync'
        stacked_on = 'base'
        stacked_type = 'nested'
        help = 'synchronize a directory with Ursa Frontier'
        arguments = [
            (['--project'], {
                 'help': 'override default project to use with this repository',
                 'dest': 'project',
                 'action': 'store'}),
            (['--dir', '--directory'], {
                 'help': 'directory to initialize (defaults to \'.\')',
                 'dest': 'directory',
                 'action': 'store',
                 'default': '.'}),
            (['--dry-run'], {
                    'help': 'rather than sync, list all resources that would be synced',
                    'dest': 'dry_run',
                    'action': 'store_true'})
        ]

    def _default(self):
        root = Path(self.app.pargs.directory)
        if not root.exists():
            print("Error: %s does not exist." % root)
            sys.exit(1)
        elif not root.is_dir():
            print("Error: %s exists and is not a directory." % root)
            sys.exit(1)

        dss_client = client('dss', self.app)
        ape_client = client('ape', self.app)
        page_client = client('page', self.app)
        planning_client = client('planning', self.app)

        resources = self._load_resources(root)

        if self.app.pargs.dry_run:
            print("Would sync:")
            print(yaml.dump({k: list(v.keys()) for k, v in resources.items() if len(v) > 0}))
            return

        # now we can sync resources
        self._sync_pages(page_client, resources['page'])
        self._sync_datasets(dss_client, resources['dataset'])
        self._sync_transforms(ape_client, resources['transform'])
        self._sync_generators(ape_client, resources['generator'])
        self._sync_pipelines(ape_client, resources['pipeline'])
        self._sync_agents(planning_client, resources['agent'])
        self._sync_packages(planning_client, resources['package'])

    def _is_synced(self, collection, path):
        if path not in collection:
            return False
        if 'published' in collection[path] and not collection[path]['published']:
            return False
        return True

    def _sync_datasets(self, client, datasets):
        for item in client.list_datasets(self._project_scope):
            if item['isSynced']:
                if not self._is_synced(datasets, item['path']):
                    client.delete_synced_dataset(item['id'])
            elif item['path'] in datasets and not item['isSynced']:
                print(f"Unable to sync dataset #{item['path']} because it is not synced.")
                datasets.delete(item['path'])
        for item in datasets.values():
            args = {
                'path': item['path'],
                'project_uuid': self._project_scope,
                'data': item['file'],
            }
            if 'contentType' in item:
                args['data_type'] = item['contentType']
            else:
                args['data_type'] = magic(item['file'])
            if 'description' in item:
                args['description'] = item['description']
            result = client.sync_dataset(**args)
            self._print(result)

    def _sync_agents(self, client, agents):
        for item in client.list_agents(self._project_scope):
            if item['isSynced']:
                if not self._is_synced(agents, item['name']):
                    client.delete_synced_agent(item['id'])
            elif item['name'] in agents and not item['isSynced']:
                print(f"Unable to sync agent #{item['name']} because it is not synced.")
                agents.delete(item['name'])
        for item in agents.values():
            args = {
                'name': item['name'],
                'project_uuid': self._project_scope,
            }

            for key in ['packages', 'behaviors']:
                if key in item:
                    args[key] = item[key]

            result = client.sync_agent(**args)
            self._print(result)

    def _sync_packages(self, client, packages):
        for item in client.list_packages(self._project_scope):
            if item['isSynced']:
                if not self._is_synced(packages, item['name']):
                    client.delete_synced_package(item['id'])
            elif item['name'] in packages and not item['isSynced']:
                print(f"Unable to sync package #{item['name']} because it is not synced.")
                packages.delete(item['name'])
        for item in packages.values():
            args = {
                'project_uuid': self._project_scope,
            }

            with open(item['file'], "r") as fd:
                args['content'] = fd.read()

            result = client.sync_package(**args)
            self._print(result)

    def _sync_pages(self, client, pages):
        for item in client.list_pages(self._project_scope):
            if item['isSynced']:
                if not self._is_synced(pages, item['path']):
                    client.delete_synced_page(item['id'])
            elif item['path'] in pages and not item['isSynced']:
                print(f"Unable to sync page #{item['path']} because it is not synced.")
                pages.delete(item['path'])
        for item in pages.values():
            args = {
                'path': item['path'],
                'content': item['content'],
                'project_uuid': self._project_scope,
            }

            for key in ['title', 'tags']:
                if key in item:
                    args[key] = item[key]

            result = client.sync_page(**args)
            self._print(result)

    def _sync_transforms(self, client, transforms):
        for item in client.list_transforms(self._project_scope):
            if not self._is_synced(transforms, item['path']):
                client.delete_synced_transform(item['id'])
            elif item['path'] in transforms and not item['isSynced']:
                print(f"Unable to sync transform #{item['path']} because it is not synced.")
                transforms.delete(item['path'])
        for item in transforms.values():
            args = {
                'path': item['path'],
                'name': item['name'],
                'type': item['type'],
                'implementation': item['implementation'],
                'configuration_schema': item['configurationSchema'],
                'project_uuid': self._project_scope,
            }
            for key in ['outputs', 'inputs', 'description', 'tags']:
                if key in item:
                    args[key] = item[key]
            result = client.sync_transform(**args)
            self._print(result)

    def _sync_generators(self, client, generators):
        for item in client.list_generators(self._project_scope):
            if not self._is_synced(generators, item['path']):
                client.delete_synced_generator(item['id'])
            elif item['path'] in generators and not item['isSynced']:
                print(f"Unable to sync generator #{item['path']} because it is not synced.")
                generators.delete(item['path'])
        for item in generators.values():
            args = {
                'path': item['path'],
                'transform': item['transform']['path'],
                'transform_configuration': item['transform']['configuration'],
                'load': item['load'],
                'project_uuid': self._project_scope
            }

            for key in ['extract', 'description', 'tags']:
                if key in item and item[key] is not None:
                    args[key] = item[key]

            result = client.sync_generator(**args)
            self._print(result)

    def _sync_pipelines(self, client, pipelines):
        for item in client.list_pipelines(self._project_scope):
            if not self._is_synced(pipelines, item['path']):
                client.delete_synced_pipeline(item['id'])
            elif item['path'] in pipelines and not item['isSynced']:
                print(f"Unable to sync pipeline #{item['path']} because it is not synced.")
                pipelines.delete(item['path'])
        for item in pipelines.values():
            args = {
                'path': item['path'],
                'project_uuid': self._project_scope
            }
            for key in ['seeders', 'generators', 'description', 'tags']:
                if key in item and item[key] is not None:
                    args[key] = item[key]

            result = client.sync_pipeline(**args)
            self._print(result)

    def _load_resources(self, root):  # noqa: C901
        # we want to look at each resource we can find locally and compute a hash
        # that makes sense for the data stored on the server - to see if there's a difference
        # for now, we're focused on the data side of things
        # we'll need to look at the planning side of things later
        # we look in each of the directories created by `init`, but use them only to
        # establish the default resource type. Resources can have a `kind` metadata
        # attribute that we can use to determin the kind of resource we're looking at.
        # datasets are special, but the same file with the .yaml extension can house
        # the metadata (so foo.csv has a foo.csv.yaml metadata file)
        #
        # OR, for datasets, we can have an index.yaml file that lists all of the datasets
        # we want to sync along with their metadata. Or both, until we find out which one
        # users find easiest to use.
        resources = {
            'agent': {},
            'package': {},
            'page': {},
            'transform': {},
            'generator': {},
            'pipeline': {},
            'dataset': {},
        }

        for file in root.rglob("*"):
            if file.is_dir():
                continue
            if file.stat().st_size == 0:
                continue
            if file.name.startswith('.'):
                continue
            info = None
            suffix = file.suffix
            default_kind = self._get_kind(root, file, {})
            if suffix == '.md':
                # likely a transform or a page
                with open(file, "r") as fd:
                    if default_kind == 'transform':
                        info = ursactl.controllers.utils.transforms.load_from_markdown(fd)
                    else:
                        info = ursactl.controllers.utils.pages.load_from_markdown(fd)
            elif suffix == '.lua':
                # likely a transform
                if file.name.endswith("_spec.lua"):
                    continue  # skip tests
                with open(file, "r") as fd:
                    info = ursactl.controllers.utils.transforms.load_from_lua(fd)
            elif suffix in ['.yaml', '.yml']:
                with open(file, "r") as fd:
                    info = list(yaml.load_all(fd, Loader=yaml.Loader))
            elif suffix == '.json':
                with open(file, "r") as fd:
                    info = json.load(fd)
            elif suffix == ".cog":
                with open(file, "r") as fd:
                    # find all the lines with "package ..." to see which packages
                    # are in this file
                    # for syncing, we expect one package per file - so error if multiple
                    info = {'name': None, 'file': file, 'kind': 'package'}
                    for line in fd.readlines():
                        if line.startswith("package"):
                            match = re.fullmatch(r"\s*package\s+(\S+)\s*([;#].*)?", line)
                            if match:
                                if info['name'] is not None:
                                    raise ValueError(f"Multiple packages found in {file}")
                                info['name'] = match.group(1)
            else:
                continue
            info = info if isinstance(info, list) else [info]
            for item in info:
                kind = self._get_kind(root, file, item)
                if kind in resources:
                    if kind in ['agent', 'package']:
                        resources[kind][item['name']] = item
                    else:
                        resources[kind][item['path']] = item
                        if kind == 'dataset':
                            resources[kind][item['path']]['file'] = file.with_name(file.stem)

        return resources

    def _get_kind(self, root, file, info) -> str:
        if info is None:
            return 'unknown'
        if 'kind' in info and info['kind'] not in [None, '']:
            return info['kind']
        if file.suffix in ['.yaml', '.yml'] and file.with_name(file.stem).exists():
            return 'dataset'
        if file.suffix == '.cog':
            return 'package'
        bits = file.relative_to(root).parts
        for type in ['agents', 'packages', 'pages', 'transforms', 'generators', 'pipelines', 'datasets']:
            if type in bits:
                return type[:-1]
        return 'unknown'

    @property
    def _project_scope(self):
        return self.app.pargs.project or self.app.config.get('ursactl', 'project')

    def _print(self, data):
        print(yaml.dump(data))
