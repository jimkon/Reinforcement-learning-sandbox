import logging
from functools import wraps
import time

from rl.src.core.configs.log_configs import *

# logging.basicConfig(filename='run_logs.txt',
#                     format='%(asctime)s %(message)s',
#                     level=logging.INFO)


def __time():
    if GENERAL_LOG_TIMINGS_FLAG:
        return time.time()
    else:
        return .0


def log(*args, tags=None, **kwargs):
    if not GENERAL_LOG_FLAG:
        return

    if isinstance(args, dict):
        msg = str(args)
    else:
        msg = "".join(list(args))
    # msg = str(args)
    print(tags, msg)
    # logging.info(msg)

class LogRun:
    pass


# https://realpython.com/primer-on-python-decorators/#decorators-with-arguments
def log_func_call(tags=None):
    TAG = "func_call"
    if not tags:
        tags = []
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
            start_time = __time()

            result = func(*args, **kwargs)

            run_time = 1000 * (__time() - start_time)
            result_str = repr(result).replace('\n', '')
            log(f"Calling: {func.__name__}( {signature} ) -> |{result_str!r}| in {run_time:.3f}", tags=tags) #

            return result
        return wrapper
    return log_tags
