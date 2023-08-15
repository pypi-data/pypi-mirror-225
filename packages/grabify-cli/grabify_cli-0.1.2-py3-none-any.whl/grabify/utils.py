import os
import json

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


def uniquify(path):
    filename, extension = os.path.splitext(path)

    counter = 1

    while os.path.exists(path):
        path = filename + " (" + str(counter) + ")" + extension
        counter += 1

    return path


def save(path, filename, image_url=None, json_data=None):
    try:
        mode = "w+"
        data = None
        distpath = ""

        path = path + ("\\" if not path.endswith("\\") else "")

        if image_url:
            data = requests.get(image_url).content
            distpath = path + filename + ".jpg"
            mode = "wb+"
        else:
            distpath = path + filename + ".json"
            data = json.dumps(json_data)

        distpath = uniquify(distpath)

        with open(distpath, mode) as f:
            f.write(data)
        
        return distpath
    except FileNotFoundError:
        os.makedirs(path)
        return save(
            path=path, filename=filename, image_url=image_url, json_data=json_data
        )

