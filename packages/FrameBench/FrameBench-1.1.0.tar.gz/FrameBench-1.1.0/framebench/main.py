from .list import list_cams
from .run import run, run_multiple

import logging
import os

import fire


def main():
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "WARNING").upper())
    logging.Logger(__name__)

    fire.Fire({
        "list": list_cams,
        "run": run,
        "run_multiple": run_multiple
    })
