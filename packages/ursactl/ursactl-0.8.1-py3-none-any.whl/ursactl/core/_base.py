

class Base:
    """
    Base class for OOP interface classes.
    """
    def __init__(self, uuid=None, client=None, app=None, project=None, **kwargs):
        self._client = client
        self._app = app
        self._uuid = uuid
        self.project = project

        if any(kwargs):
            self._cached_data = kwargs
        else:
            self._cached_data = None

    @property
    def app(self):
        if self._app is None:
            from ursactl.main import UrsaCtl
            self._app = UrsaCtl()
            self._app.reload()
        return self._app

    @property
    def uuid(self):
        return self._uuid
