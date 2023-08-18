import os

from cement import App, TestApp, init_defaults
from cement.core.exc import CaughtSignal
from cement.utils import fs
from pathlib import Path
from tinydb import TinyDB
from requests.exceptions import ConnectionError

from .controllers.base import Base
from .controllers.create import Create
from .controllers.delete import Delete
from .controllers.get import Get
from .controllers.init import Init
from .controllers.list import List
from .controllers.refresh import Refresh
from .controllers.run import Run
from .controllers.send import Send
from .controllers.show import Show
from .controllers.stop import Stop
from .controllers.sync import Sync
from .controllers.update import Update
from .core.exc import UrsaCtlError

# configuration defaults
CONFIG = init_defaults('ursactl')
CONFIG['ursactl']['cache_file'] = '~/.ursactl/.cache'
CONFIG['ursactl']['platform'] = 'https://app.ursafrontier.cloud/'


def extend_cache(app):
    app.log.info('extending with cache')
    db_file = app.config.get('ursactl', 'cache_file')

    # ensure that we expand the full path
    db_file = fs.abspath(db_file)
    app.log.info('cache file is: %s' % db_file)

    # ensure our parent directory exists
    db_dir = os.path.dirname(db_file)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)

    app.extend('db', TinyDB(db_file))


def exploded_paths():
    """
    Returns a list of directories based on the current working directory.
    Doesn't go past the home directory, if under the home directory.
    """
    cwd = os.getcwd()
    parts = cwd.split(os.path.sep)
    paths = []
    homedir = str(Path.home())

    for i in range(len(parts)):
        paths.append(os.path.sep.join(parts[:i+1]))
        paths.append(os.path.sep.join(parts[:i+1]) + '/config')
        paths.append(os.path.sep.join(parts[:i+1]) + '/.config')
        paths.append(os.path.sep.join(parts[:i+1]) + '/.ursactl')

    if any((path.startswith(homedir) for path in paths)):
        paths = [path for path in paths if path.startswith(homedir)]

    return paths


class UrsaCtl(App):
    """Ursa Frontier Control primary application."""

    class Meta:
        label = 'ursactl'

        # configuration defaults
        config_defaults = CONFIG

        # call sys.exit() on close
        exit_on_close = True

        # load additional framework extensions
        extensions = [
            'configparser',
            'colorlog',
            'tabulate'
        ]

        hooks = [
            ('post_setup', extend_cache)
        ]

        # configuration handler
        config_handler = 'configparser'

        # configuration file suffix
        config_file_suffix = '.conf'

        # configuration directories
        config_dirs = exploded_paths()

        # set the log handler
        log_handler = 'colorlog'

        # set the output handler
        output_handler = 'tabulate'

        # register handlers
        handlers = [
            Base,
            Update,
            Sync,
            Stop,
            Show,
            Send,
            Run,
            Refresh,
            List,
            Init,
            Get,
            Delete,
            Create
        ]


class UrsaCtlTest(TestApp, UrsaCtl):
    """A sub-class of UrsaCtl that is better suited for testing."""

    class Meta:
        label = 'ursactl'

    def rebuild_cache(self):
        delattr(self, 'db')
        extend_cache(self)


def main():
    with UrsaCtl() as app:
        try:
            app.run()

        except AssertionError as e:
            print('AssertionError > %s' % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback
                traceback.print_exc()

        except UrsaCtlError as e:
            print('UrsaCtlError > %s' % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback
                traceback.print_exc()

        except CaughtSignal as e:
            # Default Cement signals are SIGINT and SIGTERM, exit 0 (non-error)
            print('\n%s' % e)
            app.exit_code = 0

        except ConnectionError:
            print('Unable to connect to server')
            app.exit_code = 1


if __name__ == '__main__':
    main()
