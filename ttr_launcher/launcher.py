#!/usr/bin/env python3

# Imports {{{
# builtins
import os
import subprocess
import sys

# submodules
from ttr_launcher import (
    config,
    constants,
)
from ttr_launcher.authentication import login
from ttr_launcher.update import get_updates

# }}}


def launch_game(tokens: dict):
    print("Putting you in the game....")

    for key, value in constants.ENV.items():
        os.environ[key] = str(value)
    os.environ["TTR_GAMESERVER"] = tokens["gameserver"]
    os.environ["TTR_PLAYCOOKIE"] = tokens["cookie"]

    proc = subprocess.run([constants.GAME], cwd=constants.GAME_DIR, stdout=subprocess.PIPE)
    return proc.returncode


def main():
    launcher_config = config.ConfigHandler(constants.CONFIG_DIRECTORY)
    credentials = launcher_config.select_account(sys.argv)
    get_updates(sys.platform)
    auth_tokens = login(credentials)
    return launch_game(auth_tokens)
