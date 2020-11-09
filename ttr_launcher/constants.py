#!/usr/bin/env python3

# Imports {{{
# builtins
import logging
from platform import system
from pathlib import Path
import sys

# }}}


log = logging.getLogger(__name__)


if system() == "Darwin":
    GAME = (
        Path("~/Library/Application Support/Toontown Rewritten/Toontown Rewritten")
        .expanduser()
        .resolve()
    )
    GAME_DIR = (
        Path("~/Library/Application Support/Toontown Rewritten/").expanduser().resolve()
    )
    DYLD_LIBRARY_PATH = (
        Path("~/Library/Application Support/Toontown Rewritten/Libraries.bundle")
        .expanduser()
        .resolve()
    )
    DYLD_FRAMEWORK_PATH = (
        Path("~/Library/Application Support/Toontown Rewritten/Frameworks")
        .expanduser()
        .resolve()
    )
    CONFIG_DIRECTORY = Path("~/.config/ttrlauncher/").expanduser().resolve()
elif system() == "Linux":
    # if using the TTR snap package
    ttr_snap_dir = Path("/snap/toontown/current/")
    if ttr_snap_dir.is_dir():
        GAME = (
            Path("~/snap/toontown/common/toontown-rewritten/TTREngine")
            .expanduser()
            .resolve()
        )
        GAME_DIR = (
            Path("~/snap/toontown/common/toontown-rewritten/").expanduser().resolve()
        )
    else:
        GAME = Path("/usr/share/toontown-rewritten/TTREngine").resolve()
        GAME_DIR = Path("/usr/share/toontown-rewritten/").resolve()
    DYLD_LIBRARY_PATH = ""
    DYLD_FRAMEWORK_PATH = ""
    CONFIG_DIRECTORY = Path("~/.config/ttrlauncher/").expanduser().resolve()
elif system() == "Windows":
    # if on a 64-bit system
    if sys.maxsize > 2 ** 32:
        system = "win64"
    else:
        system = "win32"
    log.error("Windows is not yet supported.")
else:
    log.error(f'Error: Platform "{system}" not supported.')


LOGIN_URL = "https://www.toontownrewritten.com/api/login?format=json"
PATCH_MANIFEST_URL = "https://cdn.toontownrewritten.com/content/patchmanifest.txt"
CONTENT_REPO_URL = "https://cdn.toontownrewritten.com/content/"
