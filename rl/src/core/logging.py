import logging
from functools import wraps
import time

logging.basicConfig(filename='run_logs.txt',
                    format='%(asctime)s %(message)s',
                    level=logging.INFO)


def log(*args, **kwargs):

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
        start_time = time.time()
        res = func(*args, **kwargs)
        run_time = 1000 * (time.time() - start_time)
        log(f"Finished {func.__name__!r} in {run_time:.1f} ms", tag=TAG)
        return res
    return wrapper
