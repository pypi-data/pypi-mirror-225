import os
import sys


def debug_enabled():
    return os.getenv("PATCH_DEBUG", "") != ""


def debug_log(*args):
    if debug_enabled():
        print("DEBUG: ", *args, file=sys.stderr)
