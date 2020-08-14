from pathlib import Path
import logging

import click

from . import __version__
from .check import print_all_violations

logger = logging.getLogger("photos")


@click.group()
@click.version_option(__version__)
@click.option("-v", "--verbose", count=True, help="Increase logging verbosity")
def cli(verbose: int):
    logging_format = "%(asctime)14s %(levelname)-7s %(name)s - %(message)s"
    logging_level = logging.WARNING - (verbose * 10)
    logging_level_name = logging.getLevelName(logging_level)
    logging.basicConfig(format=logging_format, level=logging_level)
    logging.debug("Set logging level to %s [%d]", logging_level_name, logging_level)


@cli.command()
@click.argument("top", type=click.Path(exists=True, file_okay=False))
def check(top: str):
    """
    Check photos' organizational structure.

    Prints each violation as they are detected and summarizes by group at the end.
    """
    top = Path(top)
    logger.info("Using %s as top", top)
    children = sorted(top.iterdir(), key=lambda path: path.as_posix().casefold())
    logger.info("Found %d children", len(children))
    print_all_violations(children)
    logger.info("Done!")


main = cli.main


if __name__ == "__main__":
    main()
