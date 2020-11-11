#!/usr/bin/env python3

# Imports {{{
# builtins
import logging
from platform import system
import pathlib

# }}}


log = logging.getLogger(__name__)


def path(path: str):
    return pathlib.Path(path).expanduser().resolve()

CONFIG_DIRECTORY = path("~/.config/ttrlauncher/")

ENV = {}
if system() == "Darwin":
    GAME_DIR = (
        path("~/Library/Application Support/Toontown Rewritten/")
    )
    GAME = GAME_DIR / "Toontown Rewritten"
    ENV['DYLD_LIBRARY_PATH'] = GAME_DIR / "Libraries.bundle"
    ENV['DYLD_FRAMEWORK_PATH'] = GAME_DIR / "Frameworks"
elif system() == "Linux":
    # if using the TTR snap package
    ttr_snap_dir = path("/snap/toontown/current/")
    if ttr_snap_dir.is_dir():
        GAME_DIR = (
            path("~/snap/toontown/common/toontown-rewritten/")
        )
    else:
        GAME_DIR = path("/usr/share/toontown-rewritten/")
    GAME = GAME_DIR / "TTREngine"
elif system() == "Windows":
    GAME_DIR = path('C:/Program Files (x86)/Toontown Rewritten')
    GAME = GAME_DIR / "TTREngine.exe"
else:
    log.error(f'Error: Platform "{system}" not supported.')

LOGIN_URL = "https://www.toontownrewritten.com/api/login?format=json"
PATCH_MANIFEST_URL = "https://cdn.toontownrewritten.com/content/patchmanifest.txt"
CONTENT_REPO_URL = "https://download.toontownrewritten.com/patches/"
