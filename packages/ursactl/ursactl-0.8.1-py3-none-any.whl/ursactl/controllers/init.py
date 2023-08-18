from pathlib import Path
import sys

from cement import Controller


class Init(Controller):
    """
    Provides the 'init' verb
    """

    class Meta:
        label = 'init'
        stacked_on = 'base'
        stacked_type = 'nested'
        help = 'initialize a directory for sync with Ursa Frontier'
        arguments = [
            (['--dir', '--directory'], {
                 'help': 'directory to initialize (defaults to \'ursa\')',
                 'dest': 'directory',
                 'action': 'store',
                 'default': 'ursa'}),
        ]

    def _default(self):
        root = Path(self.app.pargs.directory)
        if not root.exists():
            root.mkdir(parents=True)
        elif not root.is_dir():
            print("Error: %s exists and is not a directory." % root)
            sys.exit(1)

        for subdir in (
                       'transforms',
                       'generators',
                       'pipelines',
                       'datasets',
                       'packages',
                       'agents',
                       'pages'
        ):
            (root / subdir).mkdir(parents=True, exist_ok=True)
            (root / subdir / '.keep').touch()
