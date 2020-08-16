from datetime import datetime
from itertools import groupby
from pathlib import Path
from typing import List, Tuple
import errno
import logging
import os

from colorama import Fore

from .metadata import read_datetime

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


def by_month(
    sources: List[Path],
    target: Path,
    dir_format: str = "%Y%m%d",
    *,
    dry_run: bool = False,
):
    """
    Group files by month, and move the files in each group into directories in `target`.
    Directories are created if needed, and are named according to the strftime-
    compatible `dir_format`, which is applied to the newest (last) photo in the group.
    """
    logger.info("Organizing %d sources into %s", len(sources), target)
    timestamps = [read_datetime(source) for source in sources]

    def key(source_timestamp: Tuple[Path, datetime]):
        _, timestamp = source_timestamp
        return timestamp.year, timestamp.month

    for _, group in groupby(sorted(zip(sources, timestamps), key=key), key=key):
        # group is a list of (source, timestamp) pairs
        group_sources, group_timestamps = zip(*group)
        max_timestamp = max(group_timestamps)
        group_dir = target / max_timestamp.strftime(dir_format)
        mkdir(group_dir, exist_ok=True, dry_run=dry_run)
        for group_source in group_sources:
            rename(group_source, group_dir / group_source.name, dry_run=dry_run)
