"""Raw commands."""

import logging
import os
import re
import shutil
import subprocess
import sys
from collections import OrderedDict
from pathlib import Path
from typing import Sequence

from .. import GRACE_ROOT
from ..utils import GraceException

logger = logging.getLogger("grace")

raw_commands: "OrderedDict[str, RawCommand]" = OrderedDict()


class RawCommand:
    """Raw command object."""

    def __init__(self, cmd: str, python: bool = False) -> None:
        """Construct a raw command object."""
        self._cmd = cmd
        self._python = python
        raw_commands[cmd] = self

    def __call__(self, args: Sequence[str], debug: bool) -> None:
        """Invoke the raw command."""
        if debug:
            cmd_args = [str(GRACE_ROOT / "bin" / "debug" / self._cmd)]
        else:
            cmd_args = [str(GRACE_ROOT / "bin" / self._cmd)]

        if self._python:
            cmd_args = [sys.executable] + cmd_args

        cmd_args += list(args)

        # We need to give the environment variables GRCMODEL and KINEMPATH.

        model_path = GRACE_ROOT / "lib" / "model"
        kinem_path = GRACE_ROOT / "lib" / "dbkinem"

        env = os.environ.copy()
        env["GRCMODEL"] = f".:{model_path}"
        env["KINEMPATH"] = f".:{kinem_path}"

        logger.info(
            f"Running subprocess: {' '.join(cmd_args)} "
            f"(GRCMODEL={env['GRCMODEL']}, KINEMPATH={env['KINEMPATH']}) ..."
        )
        try:
            subprocess.run(cmd_args, check=True, env=env)  # noqa: S603
        except subprocess.CalledProcessError as e:
            raise GraceException(
                f"command {e.cmd} returned non-zero exit status {e.returncode}"
            )
        logger.info(f"Completed subprocess: {' '.join(cmd_args)}")

        if self._cmd == "grcfort":
            patch_makefile()
        elif self._cmd == "gracefig":
            if any(a.startswith("-") for a in args):
                # NOTE: any option makes gracefig generate grcfig.eps.
                run_ps2pdf()

    @property
    def name(self) -> str:
        """Return the command name."""
        return self._cmd

    @property
    def available(self) -> bool:
        """Return `True` if the command is available."""
        # This assumes that bin and bin/debug have the same executables.
        return is_raw_command_available(self._cmd)


def patch_makefile() -> None:
    """Patch Makefile."""
    logger.info("Patching Makefile for GRACEROOT ...")

    makefile = Path("Makefile")

    if not makefile.exists():
        logger.info("Makefile not found")
        return

    lines = makefile.read_text().splitlines()

    # We need to provide GRACEROOT.

    if any(re.match(r"^\s*GRACEROOT\s*=", line) for line in lines):
        return

    for i, line in enumerate(lines):
        # Insert a line just before GRACEDIR.
        if re.match(r"^\s*GRACEDIR\s*=", line):
            lines.insert(i, f"GRACEROOT = {str(GRACE_ROOT)}")
            break
    else:
        raise RuntimeError("failed to patch Makefile")

    makefile.write_text("\n".join(lines) + "\n")

    logger.info("Completed")


def run_ps2pdf() -> None:
    """Run ps2pdf for grcfig.eps -> grcfig.pdf."""
    src_file = Path("grcfig.eps")

    if not src_file.exists():
        # gracefig should have created grcfig.eps.
        logger.warning("grcfig.eps not found")
        return

    ps2pdf = shutil.which("ps2pdf")

    if not ps2pdf:
        logger.info("ps2pdf not found")
        return

    cmd_args = (ps2pdf, src_file.name)

    logger.info(f"Running subprocess: {' '.join(cmd_args)} ...")
    try:
        subprocess.run(cmd_args, check=True)  # noqa: S603
    except subprocess.CalledProcessError as e:
        logger.warning(f"command {e.cmd} returned non-zero exit status {e.returncode}")
        return
    logger.info(f"Completed subprocess: {' '.join(cmd_args)}")


def is_raw_command_available(cmd: str, debug: bool = False) -> bool:
    """Return `True` if the given raw command is actually available."""
    if debug:
        return (GRACE_ROOT / "bin" / "debug" / cmd).is_file()
    else:
        return (GRACE_ROOT / "bin" / cmd).is_file()
