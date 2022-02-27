from functools import wraps
import cProfile, pstats, io
from pstats import SortKey

from rl.src.core.logging import log

from rl.src.core.configs.general_configs import EXPERIMENT_STORE_PERFMONITORING_DIRECTORY_ABSPATH,\
    CPROFILE_COMMAND_EXECUTION_FLAG


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

            #snakeviz ./cprofile.prof
            file = EXPERIMENT_STORE_PERFMONITORING_DIRECTORY_ABSPATH+"cprofile.prof"
            ps.dump_stats(file)
            log(f"CProfiled {func.__name__}, results in {file}")
            # with open(file, 'a') as f:
            #     ps.print_stats()
            #     f.write(s.getvalue())
            #     log(f"CProfiled {func.__name__}, results in {file}")

        return res

    return wrapper
