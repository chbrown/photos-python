from pathlib import Path
import errno
import logging
import os

from colorama import Fore

logger = logging.getLogger(__name__)

DRY_RUN_PREFIX = f"{Fore.YELLOW}[dry-run]{Fore.RESET} "


def mkdir(
    path: Path,
    mode: int = 0o777,
    parents: bool = False,
    exist_ok: bool = False,
    *,
    dry_run: bool = False,
) -> Path:
    """
    Make directory at `path`, unless `dry_run` is set, logging at INFO level.
    """
    logger.info("%sMaking directory %s", DRY_RUN_PREFIX if dry_run else "", path)
    if not dry_run:
        path.mkdir(mode=mode, parents=parents, exist_ok=exist_ok)
    return path


def rename(
    source: Path, target: Path, force: bool = False, *, dry_run: bool = False
) -> Path:
    """
    Move `source` to `target`, unless `dry_run` is set, logging at INFO level.
    If `target` exists, raise FileExistsError, unless `force` is set.
    """
    logger.info("%sMoving %s -> %s", DRY_RUN_PREFIX if dry_run else "", source, target)
    if target.exists() and not force:
        raise FileExistsError(errno.EEXIST, os.strerror(errno.EEXIST), str(target))
    if not dry_run:
        return source.rename(target)
    return source
