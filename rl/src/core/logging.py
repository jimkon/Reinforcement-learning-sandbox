import logging
from functools import wraps
import time
from os.path import join

import pandas as pd
import matplotlib.pyplot as plt

from rl.src.core.configs.log_configs import *
from rl.src.core.configs.general_configs import EXPERIMENT_STORE_LOGS_DIRECTORY_ABSPATH
from rl.src.core.utilities.file_utils import create_path
from rl.src.core.utilities.timestamp import timestamp_str, timestamp_long_str


def _time():
    if GENERAL_LOG_TIMINGS_FLAG:
        return time.time()
    else:
        return .0


class Logger:

    instances = []

    def __init__(self, name, directory=None):
        Logger.instances.append(self)

        self.name = name
        self.directory = directory if directory else ''
        self.path = join(EXPERIMENT_STORE_LOGS_DIRECTORY_ABSPATH, self.directory)

        create_path(self.path)

        self.perf_mon_path = join(self.path, PERFORMANCE_MONITORING_DIR_PATH)
        create_path(self.perf_mon_path)

        self.imgs_path = join(self.path, LOG_IMAGES_DIR_PATH)
        create_path(self.imgs_path)

        self.__log_dict = {
            "timestamp": [],
            'message': [],
            'tags': []
        }
        self.__timing_dict = {
            "timestamp": [],
            'function': [],
            'time': []
        }
        self.__img_dict = {
            "timestamp": [],
            'title': [],
            'image': []
        }

    def log(self, *args, tags=None, **kwargs):
        if not GENERAL_LOG_FLAG:
            return

        if isinstance(args, dict):
            msg = str(args)
        else:
            msg = "".join(list(args))

        tags = [] if not tags else tags if isinstance(tags, list) else [tags]
        # msg = str(args)
        if GENERAL_LOG_STDOUT_FLAG:
            print(msg, 'tags:', tags)

        self.__log_dict['timestamp'].append(timestamp_str())
        self.__log_dict['message'].append(msg)
        self.__log_dict['tags'].append('|'.join(tags))

    def log_plt(self, title=None, tags=None):
        title = f"{title}_{timestamp_str()}.png" if title else f"{timestamp_long_str()}.png"
        path = join(self.imgs_path, title)
        plt.savefig(path)

        # self.__img_dict['timestamp'].append(timestamp_str())
        # self.__img_dict['title'].append(title)
        # self.__img_dict['tags'].append(img)


    def add_timing(self, func, time_elapsed):
        self.__timing_dict['timestamp'].append(timestamp_str())
        self.__timing_dict['function'].append(func)
        self.__timing_dict['time'].append(time_elapsed)

    def save(self):
        df = pd.DataFrame(self.__timing_dict)
        df.to_csv(join(self.perf_mon_path, f"{self.name}_{CSV_FILENAME_EXTENSION_FUNCTION_TIMES_CSV}.csv"), index_label=None)

        df = pd.DataFrame(self.__log_dict)
        df.to_csv(join(self.path, f"{self.name}_{CSV_FILENAME_EXTENSION_LOGS_CSV}.csv"), index_label=None)

    # https://realpython.com/primer-on-python-decorators/#decorators-with-arguments
    def log_func_call(self, tags=None):
        TAG = "func_call"
        if not tags:
            tags = [TAG]
        elif isinstance(tags, list):
            tags.append(TAG)
        elif isinstance(tags, str):
            tags = [tags, TAG]
        else:
            tags = [TAG]

        def log_tags(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                args_repr = [repr(a) for a in args]  # 1
                kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]  # 2
                signature = ", ".join(args_repr + kwargs_repr)  # 3
                start_time = _time()

                result = func(*args, **kwargs)

                run_time = 1000.0 * (_time() - start_time)
                result_str = repr(result).replace('\n', '')
                self.log(f"Calling: {func.__name__}( {signature} ) -> |{result_str!r}| in {run_time:.3f}", tags=tags)  #
                self.add_timing(func.__name__, run_time)
                return result

            return wrapper

        return log_tags


def save_loggers():
    for _logger in Logger.instances:
        _logger.save()


logger = Logger('general')
log = logger.log
