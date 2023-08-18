from ursactl.core.services import client
from ursactl.core._base import Base


class Project(Base):
    """
    Provides access to a project and its related resources.

    When called without a project name,
    the object represents the default project as defined in the configuration.

    Parameters
    ----------
    uuid : string
        The project UUID (default: None)

    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._uuid is None:
            self._uuid = self.app.config.get('ursactl', 'project')

    @property
    def client(self):
        """
        The client used by the project object.

        :meta private:
        """
        if self._client is None:
            self._client = client('usage', self.app)
        return self._client

    @property
    def name(self):
        """The project name."""
        return self._data['name']

    @property
    def description(self):
        """The project description."""
        return self._data['description']

    @property
    def is_archived(self):
        """Whether the project is archived."""
        return self._data['isArchived']

    def Agent(self, *args, **kwargs):
        """
        Convenience method to create an agent object with the project scope.

        See :class:`ursactl.core.agent.Agent` for details.
        """
        from ursactl.core.agent import Agent as AgentClass

        return AgentClass(*args, project_uuid=self.uuid, **kwargs)

    def agents(self):
        """
        Returns a generator listing all agents belonging to the project.
        """
        from ursactl.core.agent import Agent

        if self.uuid is None:
            return []
        planning_client = client('planning', self.app)
        return (
            Agent(client=planning_client, app=self.app, project=self, **info)
            for info in planning_client.list_agents(project_scope=self.uuid)
        )

    def agent(self, name):
        """
        Returns an agent with the given name.
        """
        planning_client = client('planning', self.app)
        info = planning_client.get_agent(name, project_uuid=self.uuid)
        return self.Agent(uuid=info['id'], project=self, client=planning_client, app=self.app, **info)

    def Dataset(self, *args, **kwargs):
        """
        Convenience method to create a dataset object with the project scope.

        See :class:`ursactl.core.dataset.Dataset` for details.
        """
        from ursactl.core.dataset import Dataset as DatasetClass

        return DatasetClass(*args, project=self, app=self.app, **kwargs)

    def datasets(self):
        """
        Returns a generator listing all datasets belonging to the project.
        """
        from ursactl.core.dataset import Dataset

        if self.uuid is None:
            return []
        dss_client = client('dss', self.app)
        return (
            Dataset(client=dss_client, app=self.app, project=self, **info)
            for info in dss_client.list_datasets(project_scope=self.uuid)
        )

    def Pipeline(self, *args, **kwargs):
        """
        Convenience method to create a pipeline object with the project scope.

        See :class:`ursactl.core.pipeline.Pipeline` for details.
        """
        from ursactl.core.pipeline import Pipeline as PipelineClass

        return PipelineClass(*args, project=self, **kwargs)

    def pipelines(self):
        """
        Returns a generator listing all pipelines belonging to the project.
        """
        from ursactl.core.pipeline import Pipeline

        if self.uuid is None:
            return []
        ape_client = client('ape', self.app)
        return (
            Pipeline(client=ape_client, app=self.app, project=self, **info)
            for info in ape_client.list_pipelines(project_scope=self.uuid)
        )

    def pipeline(self, path):
        """
        Returns a pipeline with the given path.
        """
        ape_client = client('ape', self.app)
        info = ape_client.get_pipeline(path=path, project_uuid=self.uuid)
        return self.Pipeline(uuid=info['id'], client=ape_client, app=self.app, **info)

    @property
    def _data(self):
        if self._cached_data is None:
            if self.uuid is None:
                self._cached_data = {
                    'name': None,
                    'description': None,
                    'isArchived': None
                }
            else:
                self._cached_data = self.client.get_project_details(self.uuid)
        return self._cached_data
