from datetime import datetime

from rl.src.core.configs.general_configs import TIMESTAMP_STRING_FORMAT


def timestamp_str():
    return datetime.now().strftime(TIMESTAMP_STRING_FORMAT)