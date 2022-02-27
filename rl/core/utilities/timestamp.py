from datetime import datetime

from rl.core.configs.general_configs import TIMESTAMP_STRING_FORMAT,\
                                                TIMESTAMP_LONG_STRING_FORMAT
from rl.core.utilities.file_utils import unique_string


def timestamp_str():
    return datetime.now().strftime(TIMESTAMP_STRING_FORMAT)


def timestamp_long_str():
    return datetime.now().strftime(TIMESTAMP_LONG_STRING_FORMAT)


def timestamp_unique_str():
    return f"{datetime.now().strftime(TIMESTAMP_STRING_FORMAT)}_{unique_string()}"
