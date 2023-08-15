"""Copying template files."""

import logging
import shutil
from pathlib import Path
from typing import Optional, Sequence

from .. import GRACE_ROOT
from ..utils import relative_path

logger = logging.getLogger("grace")


def copy_template(name: str, destdir: Optional[Path] = None) -> None:
    """Copy a template in.prc."""
    src = GRACE_ROOT / "lib" / "templates" / name / "in.prc"
    if destdir is None:
        destdir = Path.cwd()
    dest = destdir / "in.prc"

    logger.info(f"Copying {relative_path(src)} to {relative_path(dest)} ...")

    shutil.copy(src, dest)

    logger.info("Completed")


def list_templates() -> Sequence[str]:
    """List names of templates."""
    template_dir = GRACE_ROOT / "lib" / "templates"
    names = [str(f.relative_to(template_dir)) for f in template_dir.glob("*/*")]
    return tuple(names)
