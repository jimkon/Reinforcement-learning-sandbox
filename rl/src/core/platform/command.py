from configparser import ConfigParser

from rl.src.core.logging import Logger
from rl.src.core.utilities.profiling import cprofile
from rl.src.core.configs.general_configs import RUN_CONFIGS_ABSPATH,\
                                            CPROFILE_COMMAND_EXECUTION_FLAG, \
                                            EXPERIMENT_STORE_INPUTS_OUTPUTS_DIRECTORY_ABSPATH

#
# def read_run_configs(config_path=None):
#     configs = ConfigParser()
#     configs.read(RUN_CONFIGS_ABSPATH if config_path is None else config_path)
#     return configs


def get_configs_for_command(command):
    #TODO enable multiple comfigs for different commands
    # configs = read_run_configs()
    path = EXPERIMENT_STORE_INPUTS_OUTPUTS_DIRECTORY_ABSPATH
    input_dir, output_dir = path, path
    return input_dir, output_dir


def run_command(command):
    try:
        input_dir, output_dir = get_configs_for_command(command.alias)
        cmd_obj = command(input_dir, output_dir)
        cmd_obj.input()
        cmd_obj.run()
        cmd_obj.output()
    except Exception as e:
        print(e)
        pass


# task decorator (celery or aws)
class AbstractCommand:

    alias = None
    logger = Logger(f"Command {alias}")

    @logger.log_func_call() #TODO
    def __init__(self, input_dir, output_dir):
        # TODO instantiate on-demand file loaders
        pass

    @logger.log_func_call()
    def input(self):
        #TODO read input files
        pass

    @cprofile
    @logger.log_func_call()
    def run(self):
        pass

    @logger.log_func_call()
    def output(self):
        #TODO write output to files
        pass

    def __repr__(self):
        return str(self.__class__)