from fnmatch import fnmatch
from http.client import HTTPSConnection
import io
import json
from os import path
import os
import time
from urllib import request
import zipfile

ENGINE_REPO = "MechMania-29/engine"
USER_AGENT = "MechMania-29"
FORMAT_ASSET_NAME = lambda version: f"engine-{version}.zip"
GITHUB_RELEASE_CHECK_DELAY = 60
ENGINE_DIR = "engine"
DATAFILE_NAME = "data.txt"
DATAFILE_PATH = path.join(ENGINE_DIR, DATAFILE_NAME)


def __get_current_data():
    if path.exists(DATAFILE_PATH):
        with open(DATAFILE_PATH) as file:
            data = file.read().strip()

            if data:
                data = data.split(";")

            return data


def __get_latest_release_data():
    try:
        conn = HTTPSConnection("api.github.com")
        path = f"/repos/{ENGINE_REPO}/releases/latest"
        conn.request(
            "GET",
            path,
            headers={"User-Agent": USER_AGENT},
        )

        response = conn.getresponse()

        if response.status == 200:
            data = response.read().decode("utf-8")
            release_data = json.loads(data)

            return release_data
        else:
            raise RuntimeError(
                f"`api.github.com{path}` returned status code {response.status}"
            )
    except Exception as e:
        raise RuntimeError(f"Error: Failed to connect GitHub API, {e}")


def __download(url):
    if not path.exists(ENGINE_DIR):
        os.makedirs(ENGINE_DIR, exist_ok=True)

    for filename in os.listdir(ENGINE_DIR):
        if filename != DATAFILE_NAME:
            os.remove(path.join(ENGINE_DIR, filename))

    print(f"Downloading engine from `{url}`...")

    try:
        with request.urlopen(url) as response:
            with io.BytesIO(response.read()) as zip_buffer:
                with zipfile.ZipFile(zip_buffer, "r") as zip_file:
                    zip_file.extractall(ENGINE_DIR)
    except Exception as e:
        print(f"Error downloading: {e}")

    for filename in os.listdir(ENGINE_DIR):
        if filename != DATAFILE_NAME:
            os.rename(
                os.path.join(ENGINE_DIR, filename),
                os.path.join(ENGINE_DIR, "engine.jar"),
            )

    print("Saved to `engine/engine.jar`")


def __mark_checked(checked, version):
    if not path.exists(ENGINE_DIR):
        os.makedirs(ENGINE_DIR, exist_ok=True)

    with open(DATAFILE_PATH, "w") as file:
        file.write(f"{checked};{version}")


def update_if_not_latest():
    print("Checking for latest engine...")
    data = __get_current_data()

    last_checked = float(data[0]) if data else 0
    current_version = data[1] if data else None

    checked = time.time()
    if checked - last_checked < GITHUB_RELEASE_CHECK_DELAY:
        print("Already checked recently")
        return

    release = __get_latest_release_data()
    latest_version = release["tag_name"]

    __mark_checked(checked, latest_version)

    if latest_version == current_version:
        print("Latest engine already downloaded")
        return

    print(f"New engine is available ({current_version}->{latest_version})")

    asset_url = f"https://github.com/{ENGINE_REPO}/releases/latest/download/{FORMAT_ASSET_NAME(latest_version)}"

    if not path.exists(ENGINE_DIR):
        os.makedirs(ENGINE_DIR, exist_ok=True)

    __download(asset_url)


if __name__ == "__main__":
    update_if_not_latest()
