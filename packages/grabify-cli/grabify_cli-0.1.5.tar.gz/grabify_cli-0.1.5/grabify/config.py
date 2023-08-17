"""
Grabify
~~~~~~~~~~~~~~~~~~~

A command-line tool that allows you to download
artwork and metadata from Spotify tracks and albums.

:copyright: (c) 2023 woidzero
:license: MIT, see LICENSE for more details.
"""
from pathlib import Path

__version__ = "0.1.3"
__prog_name__ = "grabify"

DEFAULT_PATH = str(Path.home()) + "\\Downloads\\grabify\\"
