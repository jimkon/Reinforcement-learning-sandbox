from os.path import splitext, join

import pandas as pd

from rl.src.core.configs.general_configs import RUN_CONFIGS_ABSPATH,\
                                            CPROFILE_COMMAND_EXECUTION_FLAG, \
                                            EXPERIMENT_STORE_INPUTS_OUTPUTS_DIRECTORY_ABSPATH
from rl.src.core.utilities.file_utils import read_json_file


def get_configs_for_command(command):
    #TODO enable multiple comfigs for different commands
    # configs = read_run_configs()
    path = EXPERIMENT_STORE_INPUTS_OUTPUTS_DIRECTORY_ABSPATH
    input_dir, output_dir = path, path
    return input_dir, output_dir


def run_command(command):
    # try: TODO
    input_dir, output_dir = get_configs_for_command(command.alias)
    cmd_obj = command(input_dir, output_dir)
    cmd_obj.input()
    cmd_obj.run()
    cmd_obj.output()
    # except Exception as e:
    #     print(e)
    #     pass


# task decorator (celery or aws)
class AbstractCommand:

    def __init__(self, input_dir, output_dir):
        self.__input_dir = join(EXPERIMENT_STORE_INPUTS_OUTPUTS_DIRECTORY_ABSPATH, input_dir)
        self.__output_dir = join(EXPERIMENT_STORE_INPUTS_OUTPUTS_DIRECTORY_ABSPATH, output_dir)

        pass

    @property
    def input_dir(self):
        return self.__input_dir

    @property
    def output_dir(self):
        return self.__output_dir

    def input(self):
        #TODO read input files
        pass

    def run(self):
        pass

    def output(self):
        #TODO write output to files
        pass

    def __repr__(self):
        return str(self.__class__)

    def read_file(self, file):
        filename, ext = splitext(file)
        ext = ext[1:] if len(ext) > 1 else None
        abspath = join(self.__input_dir, file)
        if ext is None:
            raise ValueError(f"Not recognized file {file}. Extension: {ext}")
        elif ext == 'json':
            result = read_json_file(abspath)
        elif ext == 'csv':
            raise ValueError(f"Not recognized file {file}. Extension: {ext}")
        elif ext == 'txt':
            raise ValueError(f"Not recognized file {file}. Extension: {ext}")
        else:
            raise ValueError(f"Not recognized file {file}. Extension: {ext}")

        return result

    def write_to_file(self, data, filename):
        if isinstance(data, pd.DataFrame):
            data.to_csv(join(self.__output_dir, filename), index=False)
