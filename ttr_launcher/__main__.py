#!/usr/bin/env python3

# Imports {{{
# builtins
import sys

# local modules
from ttr_launcher.launcher import main

# }}}


try:
    sys.exit(main())
except KeyboardInterrupt:
    print("Bye!")
    sys.exit(0)
