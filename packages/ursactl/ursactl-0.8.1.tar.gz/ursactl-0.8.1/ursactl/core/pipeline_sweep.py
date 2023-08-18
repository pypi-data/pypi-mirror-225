from ursactl.core.services import client
from ursactl.core._base import Base
import time
from requests.exceptions import ConnectionError

from .pipeline_run import PipelineRun


class PipelineSweep(Base):
    """
    Provides access to a pipeline sweep.
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
    def pipeline_runs(self):
        return [
            PipelineRun(
                uuid=run['id'],
                project=self.project,
                app=self.app,
                client=self.client,
                pipeline=self.pipeline,
                **run) for run in self._data['pipelineRuns']]

    @property
    def job_status(self):
        return self._data['jobStatus']

    def refresh(self):
        if self.uuid is not None:
            if self._cached_data is None:
                self._cached_data = {}
            self._cached_data.update(self.client.get_pipeline_sweep(uuid=self.uuid))

    @property
    def _data(self):
        if self._cached_data is None:
            if self.uuid is None:
                self._cached_data = {
                    'pipelineRuns': [],
                    'jobStatus': None,
                }
            else:
                self._cached_data = self.client.get_pipeline_sweep(uuid=self.uuid)
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
        return self.job_status == 'completed' and all(run.completed for run in self.pipeline_runs)
