import importlib
import argparse
from time import time
from configparser import ConfigParser
import cProfile, pstats, io
from pstats import SortKey

from rl.src.core.commands.commands import COMMANDS, get_command
from rl.src.core.platform.command import run_command
from rl.src.core.configs.general_configs import RUN_CONFIGS_ABSPATH, CPROFILE_COMMAND_EXECUTION_FLAG
from rl.src.core.logging import log


def read_run_configs():
    configs = ConfigParser()
    configs.read(RUN_CONFIGS_ABSPATH)
    return configs


def read_args():
    all_cmds_str = [cmd.alias for cmd in COMMANDS]

    parser = argparse.ArgumentParser(description='Execute the experiments defined on the run_configs.ini')
    parser.add_argument('command', help=f"Command alias to run. Options: {all_cmds_str}")
    parser.add_argument('-e', '--exp', help="Experiment's directory.", required=False)
    args = vars(parser.parse_args())
    return args



def main():

    args = read_args()
    # args = process_args(args, configs)

    log(args)

    command = get_command(args['command'])

    if CPROFILE_COMMAND_EXECUTION_FLAG:

        pr = cProfile.Profile()
        pr.enable()

        run_command(command)

        pr.disable()
        s = io.StringIO()
        sortby = SortKey.CUMULATIVE
        # sortby = SortKey.TIME
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        log(s.getvalue())
    else:
        run_command(command)


if __name__ == "__main__":
    main()


