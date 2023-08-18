"""
Dataset object providing a OOP interface to datasets.
"""
from ursactl.core.services import client
from ursactl.core._base import Base


class Dataset(Base):
    """
    Provides access to a dataset.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._content = None

    @property
    def client(self):
        if self._client is None:
            self._client = client('dss', self.app)
        return self._client

    def commit(self):
        if self.uuid is None:
            # create rather than update
            # don't support uploading data (yet)
            result = self.client.create_dataset(
                project_uuid=self.project.uuid,
                name=self.name,
                description=self.description
            )
            if result['accepted']:
                self._uuid = result['uuid']
                return True
            return False
        return False

    @property
    def path(self):
        return self._data['path']

    @property
    def description(self):
        return self._data['description']

    @property
    def content_type(self):
        return self._data['contentType']

    @property
    def size(self):
        return self._data['size']

    @property
    def url(self):
        return self._data['url']

    @property
    def content(self):
        if self._content is None and self.url is not None:
            self._content = self.client.download_dataset_content(self.url)
        return self._content

    @property
    def created_at(self):
        return self._data['createdAt']

    @property
    def updated_at(self):
        return self._data['updatedAt']

    @property
    def _data(self):
        if self._cached_data is None:
            if self.uuid is None:
                self._cached_data = {
                    'path': None,
                    'description': None,
                    'contentType': None,
                    'size': None,
                    'url': None,
                    'createdAt': None,
                    'updatedAt': None
                }
            else:
                self._cached_data = self.client.get_dataset_details(self.uuid)
                self._cached_data['url'] = self.client.get_dataset_url(self.project.uuid, self.uuid)

        return self._cached_data
