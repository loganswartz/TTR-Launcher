#!/usr/bin/env python3

# builtins
import os
import subprocess
import sys
from pathlib import Path

# submodules
import config
import update
import authentication


# initialize some constants
LOGIN_URL = "https://www.toontownrewritten.com/api/login?format=json"

system = sys.platform.lower()
if system == "darwin":
    GAME = Path("~/Library/Application Support/Toontown Rewritten/Toontown Rewritten").expanduser().resolve()
    GAME_DIR = Path("~/Library/Application Support/Toontown Rewritten/").expanduser().resolve()
    DYLD_LIBRARY_PATH = Path("~/Library/Application Support/Toontown Rewritten/Libraries.bundle").expanduser().resolve()
    DYLD_FRAMEWORK_PATH = Path("~/Library/Application Support/Toontown Rewritten/Frameworks").expanduser().resolve()
    CONFIG_DIRECTORY = Path("~/.config/ttrlauncher/").expanduser().resolve()
elif system == "linux":
    # if using the TTR snap package
    ttr_snap_dir = Path('/snap/toontown/current/')
    if ttr_snap_dir.is_dir():
        GAME = Path("~/snap/toontown/common/toontown-rewritten/TTREngine").expanduser().resolve()
        GAME_DIR = Path("~/snap/toontown/common/toontown-rewritten/").expanduser().resolve()
    else:
        GAME = Path("/usr/share/toontown-rewritten/TTREngine").resolve()
        GAME_DIR = Path("/usr/share/toontown-rewritten/").resolve()
    DYLD_LIBRARY_PATH = ""
    DYLD_FRAMEWORK_PATH = ""
    CONFIG_DIRECTORY = Path("~/.config/ttrlauncher/").expanduser().resolve()
elif system == "win32":
    # if on a 64-bit system
    if sys.maxsize > 2**32:
        system = "win64"
    else:
        system = "win32"
    die("Windows is not yet supported, sorry....")
else:
    die(f"Error: Platform \"{system}\" not supported.")


def die(reason):
    print(reason)
    exit(1)


def launch_game(tokens: dict):
    print("Putting you in the game....")
    os.environ['TTR_GAMESERVER'] = tokens['gameserver']
    os.environ['TTR_PLAYCOOKIE'] = tokens['cookie']
    os.environ['DYLD_LIBRARY_PATH'] = DYLD_LIBRARY_PATH
    os.environ['DYLD_FRAMEWORK_PATH'] = DYLD_FRAMEWORK_PATH
    subprocess.run([GAME], cwd=GAME_DIR, stdout=subprocess.PIPE)
    exit(0)


if __name__ == "__main__":
    launcher_config = config.Config_Handler(CONFIG_DIRECTORY)
    credentials = launcher_config.select_account(sys.argv)
    auth_tokens = authentication.login(credentials)
    update.get_updates(system, GAME_DIR, auth_tokens)
    launch_game(auth_tokens)

