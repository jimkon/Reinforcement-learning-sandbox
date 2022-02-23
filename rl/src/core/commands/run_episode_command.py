from rl.src.core.platform.command import AbstractCommand
from rl.src.core.utilities.profiling import cprofile
from rl.src.core.logging import Logger


# TODO
# execute experiment
class RunEpisodeCommand(AbstractCommand):

    alias = 're'
    logger = Logger(f"Command {alias}")

    @cprofile
    @logger.log_func_call()
    def run(self):
        print('RUN re')


