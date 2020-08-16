from datetime import datetime

from photos.metadata import parse_exif_datetime


def test_parse_exif_datetime():
    assert parse_exif_datetime("2001:02:03 04:05:06") == datetime(2001, 2, 3, 4, 5, 6)
