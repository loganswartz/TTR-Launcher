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
    os.environ["TTR_GAMESERVER"] = tokens["gameserver"]
    os.environ["TTR_PLAYCOOKIE"] = tokens["cookie"]
    os.environ["DYLD_LIBRARY_PATH"] = str(constants.DYLD_LIBRARY_PATH)
    os.environ["DYLD_FRAMEWORK_PATH"] = str(constants.DYLD_FRAMEWORK_PATH)
    subprocess.run([constants.GAME], cwd=constants.GAME_DIR, stdout=subprocess.PIPE)
    exit(0)


def main():
    launcher_config = config.ConfigHandler(constants.CONFIG_DIRECTORY)
    credentials = launcher_config.select_account(sys.argv)
    auth_tokens = login(credentials)
    get_updates(sys.platform, constants.GAME_DIR, auth_tokens)
    launch_game(auth_tokens)
