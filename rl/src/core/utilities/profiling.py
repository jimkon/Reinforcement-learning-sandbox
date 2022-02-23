from functools import wraps
import cProfile, pstats, io
from pstats import SortKey

from rl.src.core.logging import log

from rl.src.core.configs.general_configs import RUN_CONFIGS_ABSPATH,\
    CPROFILE_COMMAND_EXECUTION_FLAG,\
    EXPERIMENT_STORE_PERFMONITORING_DIRECTORY_ABSPATH


def cprofile(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if CPROFILE_COMMAND_EXECUTION_FLAG:
            pr = cProfile.Profile()
            pr.enable()

        res = func(*args, **kwargs)

        if CPROFILE_COMMAND_EXECUTION_FLAG:
            pr.disable()
            s = io.StringIO()
            sortby = SortKey.CUMULATIVE
            # sortby = SortKey.TIME
            ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
            file = EXPERIMENT_STORE_PERFMONITORING_DIRECTORY_ABSPATH+"cprofile.txt"
            with open(file, 'a') as f:
                ps.print_stats()
                f.write(s.getvalue())
                log(f"CProfiled {func.__name__}, results in {file}")

        return res

    return wrapper