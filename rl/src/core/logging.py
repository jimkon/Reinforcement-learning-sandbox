import logging
from functools import wraps
import time

from rl.src.core.configs.log_configs import *

logging.basicConfig(filename='run_logs.txt',
                    format='%(asctime)s %(message)s',
                    level=logging.INFO)


def __time():
    if GENERAL_LOG_TIMINGS_FLAG:
        return time.time()
    else:
        return .0


def log(*args, **kwargs):
    if not GENERAL_LOG_FLAG:
        return

    if isinstance(args, dict):
        msg = str(args)
    else:
        msg = "".join(list(args))
    # msg = str(args)
    print(msg)
    logging.info(msg)


def log_func_call(func):
    TAG = "func_call"
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = __time()
        res = func(*args, **kwargs)
        run_time = 1000 * (__time() - start_time)
        log(f"Finished {func.__name__!r} in {run_time:.1f} ms", tag=TAG)
        return res
    return wrapper
