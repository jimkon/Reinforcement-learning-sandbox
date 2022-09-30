from os import listdir
from os.path import splitext, join

import pandas as pd

from rl.core.configs.path_confgis import EXPERIMENT_ROOT_ABSPATH
from rl.core.utilities.file_utils import read_json_file, store_df, read_df


# def get_configs_for_command(command):
#     #TODO enable multiple comfigs for different commands
#     # configs = read_run_configs()
#     path = EXPERIMENT_INPUTS_OUTPUTS_DIRECTORY_ABSPATH
#     input_dir, output_dir = path, path
#     return input_dir, output_dir


def run_command(command):
    # try: TODO
    # input_dir, output_dir = get_configs_for_command(command.alias)
    # cmd_obj = command(input_dir, output_dir)
    cmd_obj = command()
    cmd_obj.input()
    cmd_obj.run()
    cmd_obj.output()
    # except Exception as e:
    #     print(e)
    #     pass


# task decorator (celery or aws)
class AbstractCommand:

    def __init__(self, input_dir, output_dir):
        self.__input_dir = join(EXPERIMENT_ROOT_ABSPATH, input_dir)
        self.__output_dir = join(EXPERIMENT_ROOT_ABSPATH, output_dir)
        pass

    @property
    def input_dir(self):
        return self.__input_dir

    @property
    def output_dir(self):
        return self.__output_dir

    def input(self):
        """
        only file input operations (read/load/etc)
        """
        #TODO read input files
        pass

    def run(self):
        pass

    def output(self):
        """
        only file output operations (write/upload to db/etc)
        """
        #TODO write output to files
        pass

    def __repr__(self):
        return str(self.__class__)

    def read_file(self, file=None):
        if file is None:
            return listdir(self.__input_dir)

        filename, ext = splitext(file)
        ext = ext[1:] if len(ext) > 1 else None
        abspath = join(self.__input_dir, file)
        if ext is None:
            raise ValueError(f"Not recognized file {file}. Extension: {ext}")
        elif ext == 'json':
            result = read_json_file(abspath)
        elif ext == 'csv':
            result = read_df(abspath)
        elif ext == 'txt':
            raise ValueError(f"Not recognized file {file}. Extension: {ext}")
        else:
            raise ValueError(f"Not recognized file {file}. Extension: {ext}")

        return result

    def write_to_file(self, data, filename):
        if isinstance(data, pd.DataFrame):
            abspath = join(self.__output_dir, filename)
            store_df(data, abspath)
        else:
            raise ValueError(f"Not recognized data type {type(data)}. end file: {filename}")

    def clean_file(self, abspath):
        # TODO append filename to be cleaned after execution
        pass
