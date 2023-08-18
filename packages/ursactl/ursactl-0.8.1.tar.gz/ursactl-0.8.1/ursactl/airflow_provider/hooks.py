from typing import Any

from airflow.exceptions import AirflowException
from airflow.hooks.base import BaseHook
from airflow.utils.log.logging_mixin import LoggingMixin

from ursactl.core.services import client


class ConfigManager:
    def __init__(self, config):
        self.sections = config

    def get(self, section, key):
        if section not in self.sections:
            return None
        if key not in self.sections[section]:
            return None
        return self.sections[section][key]


class CacheDb:
    def __init__(self):
        self.cache = []

    def insert(self, dict):
        self.cache.append(dict)

    def search(self, query):
        print(query)
        return self.cache

    def delete(self, query):
        print(query)
        self.cache = []


class UrsaCtlProviderApp:
    """
    This presents enough of the App interface for the services to work.
    """

    def __init__(self, api_key, api_secret, api_host, project):
        self.config = ConfigManager({
            "ursactl": {
                "api_key": api_key,
                "api_secret": api_secret,
                "platform": api_host,
                "project": project
            }
        })
        self.db = None

    def log(self, msg):
        self.log.info(msg)


class UrsaCtlHook(BaseHook, LoggingMixin):
    """
    Uses Ursa Frontier Platform API to send and receive datasets and run pipelines.
    """

    conn_name_attr = "ursa_frontier_conn_id"
    default_conn_name = "ursa_frontier_default"
    conn_type = "ursa_frontier_platform"
    hook_name = "Ursa Frontier"

    def __init__(self, ursa_frontier_conn_id: str = "ursa_frontier_default"):
        super().__init__()
        conn = self.get_connection(ursa_frontier_conn_id)
        self.api_key = conn.extra_dejson.get("api_key", None)
        self.api_secret = conn.extra_dejson.get("api_secret", None)
        self.api_host = conn.extra_dejson.get("platform", "app.ursafrontier.com")
        self.api_projoect = conn.extra_dejson.get("project", None)

        self.host = conn.host

        if self.api_key is None:
            raise AirflowException("api_key must be specified in the Ursa Frontier Platform connection details")

        if self.api_secret is None:
            raise AirflowException("api_secret must be specified in the Ursa Frontier Platform connection details")

        if self.api_project is None:
            raise AirflowException("project must be specified in the Ursa Frontier Platform connection details")

        self.log.info("Setting up api keys for Ursa Frontier Platform")
        app = UrsaCtlProviderApp(self.api_key, self.api_secret, self.api_host, self.api_project)
        self.dss_client = client('dss', app)
        self.ape_client = client('ape', app)

    def get_dataset(self, dataset_id, version=None):
        """
        Retrieves a dataset from the Ursa Frontier Platform.
        """
        self.log.info("Retrieving dataset %s", dataset_id)
        return self.dss_client.get_dataset(dataset_id, version)

    @staticmethod
    def get_connection_form_widgets() -> dict[str, Any]:
        """Returns connection widgets to add to connection form"""
        from flask_appbuilder.fieldwidgets import BS3PasswordFieldWidget, BS3TextFieldWidget
        from flask_babel import lazy_gettext
        from wtforms import PasswordField, StringField

        return {
            "api_host": StringField(lazy_gettext("API endpoint"), widget=BS3TextFieldWidget()),
            "api_key": StringField(lazy_gettext("API key"), widget=BS3TextFieldWidget()),
            "api_secret": PasswordField(lazy_gettext("API secret"), widget=BS3PasswordFieldWidget()),
            "api_project": StringField(lazy_gettext("Project"), widget=BS3TextFieldWidget()),
        }
