
from cement import Controller
from cement.utils.version import get_version_banner
from ..core.version import get_version

VERSION_BANNER = """
Ursa Frontier CLI. %s
%s
""" % (get_version(), get_version_banner())


class Base(Controller):
    class Meta:
        label = 'base'

        title = 'verbs'

        # text displayed at the top of --help output
        description = 'Command line control script and library for Ursa Frontier SaaS Platform.'

        # text displayed at the bottom of --help output
        epilog = 'Usage: ursactl verb ...'

        # controller level arguments. ex: 'ursactl --version'
        arguments = [
            # add a version banner
            (['-v', '--version'],
             {'action': 'version',
                'version': VERSION_BANNER}),
            (['-o', '--output'],
             {'help': 'Select an alternate output format (json, yaml)',
              'action': 'store',
              'dest': 'output'}),
        ]

    def _default(self):
        """Default action if no sub-command is passed."""

        self.app.args.print_help()
