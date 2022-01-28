from os import makedirs
from os.path import exists, split


def create_path(path):
    if "." in path:
        path = split(path)[0]

    if not exists(path):
        makedirs(path)


