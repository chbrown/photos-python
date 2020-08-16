from datetime import datetime
from pathlib import Path
from typing import Collection, Dict
import logging

import PIL
import PIL.ExifTags

logger = logging.getLogger(__name__)

EXIF2NAME = PIL.ExifTags.TAGS
NAME2EXIF = {v: k for k, v in EXIF2NAME.items()}


def read_exif_tag(path: Path, name: str) -> str:
    with PIL.Image.open(path) as image:
        exif = image.getexif()
        return exif.get(NAME2EXIF.get(name))


def read_exif_tags(path: Path, names: Collection[str] = ()) -> Dict[str, str]:
    with PIL.Image.open(path) as image:
        exif = image.getexif()
        if names:
            return {name: exif.get(NAME2EXIF.get(name)) for name in names}
        # return all tags but with remapped names
        return {EXIF2NAME[exif_id]: value for exif_id, value in exif.items()}


def parse_exif_datetime(value: str) -> datetime:
    """
    Parse Exif datetime format ("YYYY:MM:DD HH:MM:SS") (no timezone).
    """
    return datetime.strptime(value, "%Y:%m:%d %H:%M:%S")


def read_datetime(path: Path) -> datetime:
    """
    Try to read and parse the "DateTimeOriginal" Exif tag from the image at `path`.
    If that fails (e.g., `path` is not an image, or there is no such tag),
    `stat` the file and return the birthtime (and if that fails, return the mtime).
    """
    try:
        return parse_exif_datetime(read_exif_tag(path, "DateTimeOriginal"))
    except PIL.UnidentifiedImageError as exc:
        logger.debug("Could not read file as Image (%s)", exc)
    except TypeError as exc:
        logger.debug("Could not read Exif data from Image (%s)", exc)
    logger.info("Falling back to filesystem metadata for %s", path)
    sr = path.stat()
    timestamp = getattr(sr, "st_birthtime", sr.st_mtime)
    return datetime.fromtimestamp(timestamp)
