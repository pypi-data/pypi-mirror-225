from ursactl.core.services import client
from ursactl.core._base import Base
from .running_agent import RunningAgent

import json


class Agent(Base):
    """
    Provides access to an agent definition.
    """
    @property
    def client(self):
        if self._client is None:
            self._client = client('planning', self.app)
        return self._client

    @property
    def name(self):
        return self._data['name']

    @property
    def packages(self):
        return self._data['packages']

    @property
    def behaviors(self):
        return self._data['behaviors']

    def run(self, state=None, predicates=None):
        result = self.client.run_agent(
            self.uuid,
            initial_state=json.dumps(state),
            initial_predicates=json.dumps(predicates),
            project_uuid=self.project.uuid
        )

        if result['errors']:
            return None
        running_agent_id = result['result']['id']
        return RunningAgent(uuid=running_agent_id, app=self.app, client=self.client, project=self.project)

    @property
    def _data(self):
        if self._cached_data is None:
            if self.uuid is None:
                self._cached_data = {
                    'name': None,
                    'packages': None,
                    'behaviors': None,
                    'project_uuid': None
                }
            else:
                self._cached_data = self.client.get_agent(self.uuid)
        return self._cached_data
