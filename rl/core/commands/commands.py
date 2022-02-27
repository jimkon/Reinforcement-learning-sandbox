from rl.core.commands.run_episode_command import RunEpisodeCommand

COMMANDS = [
    RunEpisodeCommand
]


def get_command(alias):
    for cmd in COMMANDS:
        if cmd.alias == alias:
            return cmd
    raise ValueError(f"Command {alias} does not exist. Command options: {[cmd.alias for cmd in COMMANDS]}")
