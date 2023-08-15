"""GRACE commands."""

from . import template as template  # noqa: F401  # reexport for mypy
from .raw import RawCommand
from .raw import raw_commands as raw_commands  # noqa: F401  # reexport for mypy

gracefig = RawCommand("gracefig")
grc = RawCommand("grc")
grccut = RawCommand("grccut")
grcdraw = RawCommand("grcdraw")
grcext = RawCommand("grcext", python=True)
grcfort = RawCommand("grcfort")
grcmdl = RawCommand("grcmdl")
grcmom = RawCommand("grcmom")
grcplot = RawCommand("grcplot")
grcprc = RawCommand("grcprc")
qcdcut = RawCommand("qcdcut")
tread = RawCommand("tread")
