from ursactl.core.services import client
from ursactl.core._base import Base
from .pipeline_run import PipelineRun
from .pipeline_sweep import PipelineSweep


class Pipeline(Base):
    """
    Provides access to a pipeline definition.
    """
    @property
    def client(self):
        if self._client is None:
            self._client = client('ape', self.app)
        return self._client

    @property
    def name(self):
        return self._data['name']

    @property
    def description(self):
        return self._data['description']

    @property
    def pipeline_runs(self):
        return []

    @property
    def pipeline_sweeps(self):
        return []

    def run(self, parameters=None):
        """
        Runs the pipeline, returning a PipelineRun object.
        """
        result = self.client.run_pipeline(
            self.uuid,
            parameters=parameters,
            project_uuid=self.project.uuid)

        return PipelineRun(pipeline=self, project=self.project, uuid=result['id'], app=self.app, client=self.client)

    def sweep(self, parameters=None, sweep_parameters=None):
        """
        Sweeps the pipeline, returning a PipelineSweep object.
        """
        result = self.client.run_pipeline(
            self.uuid,
            parameters=parameters,
            sweep_parameters=sweep_parameters,
            project_uuid=self.project.uuid)

        return PipelineSweep(
            pipeline=self,
            project=self.project,
            uuid=result['result']['id'],
            app=self.app,
            client=self.client)

    @property
    def _data(self):
        if self._cached_data is None:
            if self.uuid is None:
                self._cached_data = {
                    'path': None,
                    'description': None,
                    'seeders': [],
                    'generators': []
                }
            else:
                self._cached_data = self.client.get_pipeline(uuid=self.uuid)
        return self._cached_data
