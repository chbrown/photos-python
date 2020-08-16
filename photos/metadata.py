from datetime import datetime
from pathlib import Path
from typing import Collection, Dict

import PIL
import PIL.ExifTags

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
