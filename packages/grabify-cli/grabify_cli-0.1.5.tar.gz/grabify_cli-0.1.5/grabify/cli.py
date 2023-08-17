"""
Grabify
~~~~~~~~~~~~~~~~~~~

A command-line tool that allows you to download
artwork and metadata from Spotify tracks and albums.

:copyright: (c) 2023 woidzero
:license: MIT, see LICENSE for more details.
"""
import click
import requests
from bs4 import BeautifulSoup
from rich.console import Console

from .config import DEFAULT_PATH, __prog_name__, __version__
from .utils import save, theme

console = Console(theme=theme)


@click.group("grabify")
@click.version_option(__version__, "-V", "--version", prog_name=__prog_name__)
def grabify() -> None:
    """A command-line tool that allows you to download
    artwork and metadata from Spotify tracks and albums.
    """


@click.command("art")
@click.argument("url")
@click.option("--path", "-p", help="Set download path", default=DEFAULT_PATH)
def _art(url, path) -> None:
    """Downloads album/playlist/track artwork"""
    try:
        image_url = ""
        name = ""

        response = requests.get(url, timeout=60)
        soup = BeautifulSoup(response.text, features="lxml")

        for meta in soup.find_all("meta"):
            if meta.get("property") == "og:title":
                name = meta.get("content")
            if meta.get("property") == "og:image":
                image_url = meta.get("content")

        if (image_url, name) is None:
            console.print("[err]✖[/] Cannot find album name and artwork")

        saved_path = save(path, name, image_url=image_url)
        console.print(f"[ok]✔[/] Saved to {saved_path}")
    except requests.exceptions.MissingSchema:
        console.print("[err]✖[/] Incorrect URL")
    except requests.exceptions.Timeout:
        console.print("[err]✖[/] Connection timed out, try again later")


@click.command("data")
@click.argument("url")
@click.option("--path", "-p", help="Set download path", default=DEFAULT_PATH)
def _data(url: str, path: str) -> None:
    """Downloads album/playlist/track metadata"""
    try:
        name = ""
        image_url = ""
        desc = ""
        _type = ""
        raw_data = ""

        response = requests.get(url, timeout=60)
        soup = BeautifulSoup(response.text, features="lxml")

        for meta in soup.find_all("meta"):
            if meta.get("property") == "og:title":
                name = meta.get("content")
            if meta.get("property") == "og:image":
                image_url = meta.get("content")
            if meta.get("property") == "og:description":
                raw_data = meta.get("content")
            if meta.get("property") == "og:type":
                _type = meta.get("content")

            if (image_url, name, desc) is None:
                console.print("[err]✖[/] Failed to fetch data")

        data = str(raw_data).split(" · ")

        data_dict = {
            "name": name,
            "image_url": image_url,
            "type": _type,
            "author": data[0],
            "year": data[2],
            "songs": int(data[-1].replace("songs", "").replace(".", "")),
        }

        if _type == "music.playlist":
            del data_dict["year"]
            del data_dict["author"]

            data_dict.update({"songs": int(data[-1].replace("songs", ""))})

        elif _type == "music.song":
            del data_dict["songs"]

        saved_path = save(path, name.lower().replace(" ", "_"), json_data=data_dict)
        console.print(f"[ok]✔[/] Saved to {saved_path}")
    except requests.exceptions.MissingSchema:
        console.print("[err]✖[/] Incorrect URL")
    except requests.exceptions.Timeout:
        console.print("[err]✖[/] Connection timed out, try again later")


COMMANDS = (_art, _data)
