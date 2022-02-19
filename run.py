import importlib
import argparse
from time import time
from configparser import ConfigParser

from rl.src.core.commands.commands import COMMANDS
from rl.src.core.configs.general_configs import RUN_CONFIGS_ABSPATH
from rl.src.core.logging import log


def read_run_configs():
    configs = ConfigParser()
    configs.read(RUN_CONFIGS_ABSPATH)
    return configs


def read_args():
    all_cmds_str = [cmd.alias for cmd in COMMANDS]

    parser = argparse.ArgumentParser(description='Execute the experiments defined on the run_configs.ini')
    parser.add_argument('command', help=f"Command to run. Options: {all_cmds_str}")
    parser.add_argument('-e', '--exp', help="Experiment's directory.", required=False)
    args = vars(parser.parse_args())
    return args


def main():
    configs = read_run_configs()

    args = read_args()
    # args = process_args(args, configs)

    print(args)

    # module = importlib.import_module(args['module_name'])
    # iters = args['iters']
    #
    # start_time = time()
    # log(f"Execution starts. Iterations {iters}")
    # for i in range(iters):
    #     run_experiment = module.run_experiment
    #
    #     log(f"Experiment {i} starts.")
    #     exp_start_time = time()
    #     run_experiment()
    #     exp_end_time = time() - exp_start_time
    #     log(f"Experiment {i} ended in {exp_end_time} seconds.")
    #
    # end_time = time() - start_time
    # log(f"Execution ended in {end_time} seconds. Iterations {i + 1}/{iters}")


if __name__ == "__main__":
    main()

# import cProfile, pstats, io
# from pstats import SortKey
#
# pr = cProfile.Profile()
# pr.enable()

# run command

# pr.disable()
# s = io.StringIO()
# sortby = SortKey.CUMULATIVE
# # sortby = SortKey.TIME
# ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
# ps.print_stats()
# print(s.getvalue())
