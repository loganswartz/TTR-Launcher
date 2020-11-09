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
from ttr_launcher.constants import PATCH_MANIFEST_URL, CONTENT_REPO_URL

# }}}


log = logging.getLogger(__name__)


def get_updates(platform: str, game_dir: Path, auth_tokens):
    file_manifest = requests.get(PATCH_MANIFEST_URL).json()

    for filename, file in file_manifest.items():
        # if the file is needed for your system and the hashes don't match
        if platform not in file["only"]:
            pass
        elif platform in file["only"] and get_hash(game_dir / filename) != file["hash"]:
            log.info(f"Update found for {filename}. Downloading....")
            update_file(filename, file, game_dir, auth_tokens)
        else:
            log.info(f"{filename} is already up to date.")

    log.info("All updates finished.")


def update_file(filename: str, file: dict, game_dir: Path, auth_tokens):
    archive = requests.get(CONTENT_REPO_URL + file["dl"]).content
    with open(
        game_dir / filename, "wb+"
    ) as fp:  # save the fetched asset after decompressing
        compressed = bz2.decompress(archive)
        fp.write(compressed)
    if (
        get_hash(game_dir / filename) != file["hash"]
    ):  # verify downloaded file integrity
        log.warning(f"Integrity check failed. Redownloading {filename}....")
        return update_file(filename, file, game_dir, auth_tokens)
    else:
        log.info(f"{filename} was successfully updated.")
        return True


def get_hash(file: Path):
    hash = hashlib.sha1()
    with file.open(mode="rb") as f:
        while True:
            block = f.read(hash.block_size)
            if not block:
                break
            hash.update(block)
    # print(f"SHA1 hash: {hash.hexdigest()}")
    return hash.hexdigest()
