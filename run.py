import argparse


from rl.src.core.commands.commands import COMMANDS, get_command
from rl.src.core.platform.command import run_command
from rl.src.core.logging import log


def read_args():
    all_cmds_str = [cmd.alias for cmd in COMMANDS]

    parser = argparse.ArgumentParser(description='Execute the experiments defined on the run_configs.ini')
    parser.add_argument('command', help=f"Command alias to run. Options: {all_cmds_str}")
    parser.add_argument('-e', '--exp', help="Experiment's directory.", required=False)
    parser.add_argument('-c', '--config', help="Config file to use[NOT IMPLEMENTED YET].", required=False)
    args = vars(parser.parse_args())
    return args


def main():

    args = read_args()
    # args = process_args(args, configs)

    log(f"run args {args}")

    command = get_command(args['command'])

    run_command(command)


if __name__ == "__main__":
    main()


