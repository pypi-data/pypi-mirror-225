"""
Exception classes for Ursactl
"""


class UrsaCtlError(Exception):
    """Generic errors."""
    pass


class UrsaNotAuthorized(UrsaCtlError):
    """Authentication/authorization errors."""
    pass


class UrsaProjectNotDefined(UrsaCtlError):
    """Project required but not defined."""
    pass
