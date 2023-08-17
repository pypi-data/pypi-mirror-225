"""
Grabify
~~~~~~~~~~~~~~~~~~~

A command-line tool that allows you to download
artwork and metadata from Spotify tracks and albums.

:copyright: (c) 2023 woidzero
:license: MIT, see LICENSE for more details.
"""
import json
import os
from typing import Optional

import requests
from rich.theme import Theme

theme = Theme(
    {
        "info": "bold blue",
        "warn": "bold yellow",
        "err": "bold red",
        "ok": "bold green",
    }
)


def uniquify(path: str):
    """Uniquify file if dublicate"""
    filename, extension = os.path.splitext(path)

    counter = 1

    while os.path.exists(path):
        path = filename + " (" + str(counter) + ")" + extension
        counter += 1

    return path


def save(
    path: str,
    filename: str,
    image_url: Optional[str] = None,
    json_data: Optional[dict] = None,
):
    """Save file into path"""
    try:
        mode = "w+"
        data = None
        distpath = ""

        path = path + ("\\" if not path.endswith("\\") else "")

        if image_url:
            data = requests.get(image_url, timeout=60).content
            distpath = path + filename + ".jpg"
            mode = "wb+"
        else:
            distpath = path + filename + ".json"
            data = json.dumps(json_data)

        distpath = uniquify(distpath)

        with open(distpath, mode, encoding="utf-8") as file:
            file.write(data)

        return distpath
    except FileNotFoundError:
        os.makedirs(path)
        return save(
            path=path, filename=filename, image_url=image_url, json_data=json_data
        )
