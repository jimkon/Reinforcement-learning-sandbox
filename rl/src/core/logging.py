import logging
from functools import wraps
import time
from os.path import join

import pandas as pd

from rl.src.core.configs.log_configs import *
from rl.src.core.configs.general_configs import EXPERIMENT_STORE_LOGS_DIRECTORY_ABSPATH
from rl.src.core.utilities.file_utils import create_path

# logging.basicConfig(filename='run_logs.txt',
#                     format='%(asctime)s %(message)s',
#                     level=logging.INFO)


def _time():
    if GENERAL_LOG_TIMINGS_FLAG:
        return time.time()
    else:
        return .0


# def log(*args, tags=None, **kwargs):
#     if not GENERAL_LOG_FLAG:
#         return
#
#     if isinstance(args, dict):
#         msg = str(args)
#     else:
#         msg = "".join(list(args))
#     # msg = str(args)
#     print(tags, msg)
#     # logging.info(msg)


class __Logger:
    def __init__(self, name):
        self.name = name
        self.path = join(EXPERIMENT_STORE_LOGS_DIRECTORY_ABSPATH, self.name)
        self.__log_dict = {
            'message': [],
            'tags': []
        }
        self.__timing_dict = {
            'function': [],
            'time': []
        }
        pass

    def log(self, *args, tags=None, **kwargs):
        if not GENERAL_LOG_FLAG:
            return

        if isinstance(args, dict):
            msg = str(args)
        else:
            msg = "".join(list(args))

        tags = [] if not tags else tags if isinstance(tags, list) else [tags]
        # msg = str(args)
        print(msg, 'tags:', tags)
        self.__log_dict['message'].append(msg)
        self.__log_dict['tags'].append('|'.join(tags))
        # logging.info(msg)

    def add_timing(self, func, time_elapsed):
        self.__timing_dict['function'].append(func)
        self.__timing_dict['time'].append(time_elapsed)

    def save(self):
        create_path(self.path)

        df = pd.DataFrame(self.__timing_dict)
        df.to_csv(join(self.path, 'function_times.csv'), index_label=None)

        df = pd.DataFrame(self.__log_dict)
        df.to_csv(join(self.path, 'all_logs_df.csv'), index_label=None)

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


logger = None


def set_logger(name):
    global logger, log
    logger = __Logger(name)

    return logger


set_logger('default')


