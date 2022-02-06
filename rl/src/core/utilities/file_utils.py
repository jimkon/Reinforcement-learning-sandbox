from os import makedirs
from os.path import exists, split
import uuid

from rl.src.core.configs.storage_configs import UNIQUE_STRING_LENGHT


def create_path(path):
    if "." in path:
        path = split(path)[0]

    if not exists(path):
        makedirs(path)


def unique_string():
    return uuid.uuid4().hex[:UNIQUE_STRING_LENGHT].upper()
