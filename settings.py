import sys

import pathlib
import pytoml as toml

from loguru import logger

BASE_DIR = pathlib.Path(__file__).parent


def load_settings() -> dict:
    try:
        with open(pathlib.Path.joinpath(BASE_DIR, 'settings.toml')) as f:
            conf = toml.load(f)
            return conf
    except OSError as e:
        logger.error(e)
        sys.exit(1)
