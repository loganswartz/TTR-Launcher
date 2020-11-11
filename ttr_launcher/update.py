#!/usr/bin/env python3

# Imports {{{
# builtins
import bz2
import hashlib
import logging
from pathlib import Path

# 3rd party modules
import requests

# local modules
from ttr_launcher.constants import PATCH_MANIFEST_URL, CONTENT_REPO_URL, GAME_DIR

# }}}


log = logging.getLogger(__name__)


def get_updates(platform: str):
    file_manifest = requests.get(PATCH_MANIFEST_URL).json()

    for filename, file in file_manifest.items():
        # if the file is needed for your system and the hashes don't match
        if platform not in file["only"]:
            pass
        elif platform in file["only"] and not (GAME_DIR / filename).exists():
            log.info(f"Downloading {filename}....")
            update_file(filename, file)
        elif platform in file["only"] and get_hash(GAME_DIR / filename) != file["hash"]:
            log.info(f"Update found for {filename}. Downloading....")
            update_file(filename, file)
        else:
            log.info(f"{filename} is already up to date.")

    log.info("All updates finished.")


def update_file(filename: str, file: dict):
    resp = requests.get(CONTENT_REPO_URL + file["dl"])
    archive = resp.content
    saved = GAME_DIR / filename

    with saved.open("wb+") as fp:
        # save the fetched asset after decompressing
        compressed = bz2.decompress(archive)
        fp.write(compressed)

    # verify downloaded file integrity
    if get_hash(saved) != file["hash"]:
        log.warning(f"Integrity check failed. Redownloading {filename}....")
        return update_file(filename, file)
    else:
        log.info(f"{filename} was successfully updated.")
        return True


def get_hash(file: Path):
    hash = hashlib.sha1()
    with file.open(mode="rb") as fp:
        while True:
            block = fp.read(hash.block_size)
            if not block:
                break
            hash.update(block)
    # print(f"SHA1 hash: {hash.hexdigest()}")
    return hash.hexdigest()
