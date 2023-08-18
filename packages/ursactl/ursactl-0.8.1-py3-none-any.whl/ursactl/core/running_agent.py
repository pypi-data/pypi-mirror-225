from ursactl.core.services import client
from ursactl.core._base import Base


class RunningAgent(Base):
    """
    Provides access to a running agent.
    """
    @property
    def client(self):
        if self._client is None:
            self._client = client('planning', self.app)
        return self._client

    def send_event(self, domain, name, params):
        result = self.client.send_event_to_agent(
            self.uuid,
            {
                'domain': domain,
                'name': name,
                'params': params
            }
        )
        return result['result']

    def send_events(self, events):
        actions = []
        for event in events:
            result = self.client.send_event_to_agent(self.uuid, event)
            if result['result']:
                actions.extend(result['result'])
        return actions

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.client.stop_agent(self.uuid)
