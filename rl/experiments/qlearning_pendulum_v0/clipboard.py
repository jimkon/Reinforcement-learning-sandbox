import multiprocessing as mp
import time

class AbstractCommand:

    alias = None

    # @logger.log_func_call() #TODO
    def __init__(self, input_dir, output_dir):
        # TODO instantiate on-demand file loaders
        pass

    # @logger.log_func_call()
    def input(self):
        print("Abs __input")
        #TODO read input files
        pass

    # @cprofile
    # @logger.log_func_call()
    def run(self):
        print('ABs __run')
        pass

    # @logger.log_func_call()
    def output(self):
        #TODO write output to files
        pass

class RunEpisodeCommand(AbstractCommand):

    alias = 're'

    def run(self):
        print('RUN re')

if __name__ == '__main__':
    cmd = AbstractCommand(None, None)
    print(dir(cmd))
    re = RunEpisodeCommand(None, None)
    print(dir(re))
    re.input()
    re.run()

