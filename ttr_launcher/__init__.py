#!/usr/bin/env python3

# Imports {{{
# builtins
import logging
import pathlib
import sys

# }}}


# setup logging
module_name = pathlib.Path(__file__).resolve().parent.name
log = logging.getLogger(module_name)
log.setLevel(logging.INFO)
sh = logging.StreamHandler(sys.stdout)
sh.setLevel(logging.DEBUG)
log.addHandler(sh)
