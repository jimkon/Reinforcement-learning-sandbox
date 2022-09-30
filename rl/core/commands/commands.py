from rl.core.commands.run_episode_command import RunEpisodeCommand
from rl.core.commands.process_results import ProcessResultsCommand

COMMANDS = [
    RunEpisodeCommand,
    ProcessResultsCommand
]


def get_command(alias):
    for cmd in COMMANDS:
        if cmd.alias == alias:
            return cmd
    raise ValueError(f"Command {alias} does not exist. Command options: {[cmd.alias for cmd in COMMANDS]}")
