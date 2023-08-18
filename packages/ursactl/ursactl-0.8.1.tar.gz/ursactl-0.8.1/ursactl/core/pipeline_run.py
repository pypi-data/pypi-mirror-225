from ursactl.core.services import client
from ursactl.core._base import Base
import time


class PipelineRun(Base):
    """
    Provides access to a pipeline run.
    """
    def __init__(self, *args, pipeline=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.pipeline = pipeline

    @property
    def client(self):
        if self._client is None:
            self._client = client('ape', self.app)
        return self._client

    @property
    def job_status(self):
        return self._data['jobStatus']

    @property
    def provenance(self):
        return self._data['provenance']

    @property
    def parameters(self):
        return self._data['parameters']

    @property
    def dataset(self):
        if self._data['dataset']:
            return self.project.Dataset(uuid=self._data['dataset']['id'])

    def refresh(self):
        if self.uuid is not None:
            self._cached_data = self.client.get_pipeline_run(uuid=self.uuid)

    @property
    def _data(self):
        if self._cached_data is None:
            if self.uuid is None:
                self._cached_data = {
                    'dataset': None,
                    'jobStatus': None,
                    'provenance': None,
                    'parameters': None,
                }
            else:
                self._cached_data = self.client.get_pipeline_run(uuid=self.uuid)
        return self._cached_data

    def __enter__(self):
        while not self.completed:
            time.sleep(5)
            try:
                self.refresh()
            except ConnectionError:
                pass
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    @property
    def completed(self):
        return self.job_status == 'completed'
