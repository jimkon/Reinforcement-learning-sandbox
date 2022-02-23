from rl.src.core.platform.command import AbstractCommand


# TODO
# execute experiment
class RunEpisodeCommand(AbstractCommand):

    alias = 're'

    def run(self):
        print('RUN re')


# if __name__=="__main__":
#     RunEpisodeCommand()
