"""A Python wrapper for the GRACE system."""

import pathlib

from .version import __version__ as __version__  # noqa: F401  # reexport for mypy

GRACE_ROOT = pathlib.Path(__file__).parent
