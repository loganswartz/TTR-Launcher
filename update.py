#!/usr/bin/env python3

# builtins
import json
from pathlib import Path
import hashlib
import bz2

# 3rd party modules
import requests


def get_updates(system_platform: str, game_dir: Path, auth_tokens):
    file_manifest = requests.get('https://cdn.toontownrewritten.com/content/patchmanifest.txt').json()

    for filename, file in file_manifest.items():
        # if the file is needed for your system and the hashes don't match
        if system_platform not in file['only']:
            pass
        elif system_platform in file['only'] and get_hash(game_dir / filename) != file['hash']:
            print(f"Update found for {filename}. Downloading....")
            update_file(filename, file, game_dir, auth_tokens)
        else:
            print(f"{filename} is already up to date.")

    print("All updates finished.")


def update_file(filename: str, file: dict, game_dir: Path, auth_tokens):
    archive = requests.get(f"https://cdn.toontownrewritten.com/content/{file['dl']}").content
    with open(game_dir / filename, 'w+') as outfile:  # save the fetched asset after decompressing
        outfile.write(bz2.decompress(archive))
    if get_hash(game_dir / filename) != file['hash']:  # verify downloaded file integrity
        print(f"Integrity check failed. Redownloading {filename}....")
        return update_file(filename, file, game_dir)
    else:
        print(f"{filename} was successfully updated.")
        return True


def get_hash(file: Path):
    hash = hashlib.sha1()
    with file.open(mode='rb') as f:
        while True:
            block = f.read(hash.block_size)
            if not block:
                break
            hash.update(block)
    #print(f"SHA1 hash: {hash.hexdigest()}")
    return hash.hexdigest()

