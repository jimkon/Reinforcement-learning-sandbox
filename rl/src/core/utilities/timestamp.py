from datetime import datetime

from rl.src.core.configs.general_configs import TIMESTAMP_STRING_FORMAT,\
                                                TIMESTAMP_LONG_STRING_FORMAT
from rl.src.core.utilities.file_utils import unique_string

def timestamp_str():
    return datetime.now().strftime(TIMESTAMP_STRING_FORMAT)


def timestamp_long_str():
    return datetime.now().strftime(TIMESTAMP_LONG_STRING_FORMAT)


def timestamp_unique_str():
    return f"{unique_string()}_{datetime.now().strftime(TIMESTAMP_STRING_FORMAT)}"
