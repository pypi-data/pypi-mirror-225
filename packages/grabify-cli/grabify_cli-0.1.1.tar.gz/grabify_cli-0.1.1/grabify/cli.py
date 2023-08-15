import requests
from bs4 import BeautifulSoup
from rich.console import Console

from . import __version__, __prog_name__
from .config import Config
from .utils import save, theme

import click

console = Console(theme=theme)


@click.group("grabify")
@click.version_option(__version__, "-V", "--version", prog_name=__prog_name__)
def grabify():
    """
    A command-line tool that allows you to download
    artwork and metadata from Spotify tracks and albums.
    """
    pass


@click.command()
@click.argument("url")
@click.option("--path", "-p", help="Set download path", default=Config.DEFAULT_PATH)
def art(url, path):
    image_url = ""
    name = ""

    try:
        response = requests.get(url, timeout=60)
    except requests.exceptions.MissingSchema:
        console.print("[err]✖[/] Incorrect URL")
    except requests.exceptions.Timeout:
        console.print("[err]✖[/] Connection timed out, try again later")

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


@click.command()
@click.argument("url")
@click.option("--path", "-p", help="Set download path", default=Config.DEFAULT_PATH)
def data(url: str, path: str):
    name = ""
    image_url = ""
    desc = ""
    _type = ""
    raw_data = ""

    try:
        response = requests.get(url, timeout=60)
    except requests.exceptions.MissingSchema:
        console.print("[err]✖[/] Incorrect URL")
    except requests.exceptions.Timeout:
        console.print("[err]✖[/] Connection timed out, try again later")

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

    year = data[2]
    author = data[0]

    songs = int(data[-1].replace("songs", "").replace(".", ""))

    data_dict = {
        "name": name,
        "image_url": image_url,
        "type": _type,
        "author": author,
        "year": year,
        "songs": songs,
    }

    if _type == "music.playlist":
        del data_dict["year"]
        del data_dict["author"]

        data_dict.update({"songs": int(data[-1].replace("songs", ""))})

    elif _type == "music.song":
        del data_dict["songs"]
        
    name = name.lower().replace(" ", "_")

    saved_path = save(path, name, json_data=data_dict)
    console.print(f"[ok]✔[/] Saved to {saved_path}")


COMMANDS = (art, data)
