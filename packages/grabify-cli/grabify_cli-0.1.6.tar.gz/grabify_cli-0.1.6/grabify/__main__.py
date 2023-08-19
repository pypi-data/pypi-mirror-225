"""
Grabify
~~~~~~~~~~~~~~~~~~~

A command-line tool that allows you to download
artwork and metadata from Spotify tracks and albums.

:copyright: (c) 2023 woidzero
:license: MIT, see LICENSE for more details.
"""
import sys

import click

from .cli import COMMANDS, grabify

for cmd in COMMANDS:
    grabify.add_command(cmd)


def main() -> click.Group:
    """Program entry point."""
    return grabify()


if __name__ == "__main__":
    sys.exit(main())  # type: ignore
