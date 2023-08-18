
from ursactl.main import UrsaCtlTest


def test_ursactl():
    # test ursactl without any subcommands or arguments
    with UrsaCtlTest() as app:
        app.run()
        assert app.exit_code == 0


def test_ursactl_debug():
    # test that debug mode is functional
    argv = ['--debug']
    with UrsaCtlTest(argv=argv) as app:
        app.run()
        assert app.debug is True
