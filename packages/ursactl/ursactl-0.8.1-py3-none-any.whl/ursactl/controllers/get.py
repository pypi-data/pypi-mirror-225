from cement import Controller, ex

from ..core.services import client


class Get(Controller):
    '''
    Provides the 'get' verb.
    '''

    class Meta:
        label = 'get'
        stacked_on = 'base'
        stacked_type = 'nested'
        help = 'get something'

    @ex(help='download dataset',
        arguments=[
            (['--project'], {'help': 'project identifier', 'dest': 'project', 'action': 'store'}),
            (['dataset'], {'help': 'UUID or path of the dataset to download', 'action': 'store'}),
            (['destination'], {'help': 'local file in which the dataset is saved', 'action': 'store'})
        ])
    def dataset(self):
        dataset_uuid = self.app.pargs.dataset
        destination = self.app.pargs.destination
        dss_client = client('dss', self.app)
        url = dss_client.get_dataset_url(project_uuid=self._project_scope, dataset=dataset_uuid)
        if url is None:
            exit(1)
        if not dss_client.download_dataset(url, destination):
            exit(1)

    @property
    def _project_scope(self):
        return self.app.pargs.project or self.app.config.get('ursactl', 'project')
