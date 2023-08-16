try:
    from anaconda_cloud_cli._version import version as __version__
except ImportError:  # pragma: nocover
    __version__ = "unknown"

from anaconda_cli_base import console

__all__ = ["__version__", "console"]
