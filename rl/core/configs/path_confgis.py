from os import makedirs
from os.path import exists, split, join, isfile
from configparser import ConfigParser


def create_path(path, *args):
    path = join(path, *args)

    if isfile(path):
        path = split(path)[0]

    if not exists(path):
        makedirs(path)

    return path


ROOT_DIRECTORY = "Reinforcement-learning-sandbox"
ROOT_ABSPATH = join(__file__.split(ROOT_DIRECTORY)[0], ROOT_DIRECTORY)
print("PROJECT_DIRECTORY", ROOT_ABSPATH)

RUN_CONFIGS_FILENAME = 'run_config.ini'
RUN_CONFIGS_ABSPATH = join(ROOT_ABSPATH, RUN_CONFIGS_FILENAME)
print("RUN_CONFIGS_ABSPATH", RUN_CONFIGS_ABSPATH)

__configs = ConfigParser()
__configs.read(RUN_CONFIGS_ABSPATH)


EXPERIMENT_ROOT_DIRECTORY = join(__configs['DEFAULTS']['experiments_dir'],
                                 __configs['EXPERIMENT']['module'])
EXPERIMENT_ROOT_ABSPATH = join(ROOT_ABSPATH, EXPERIMENT_ROOT_DIRECTORY)
print("EXPERIMENT_ROOT_ABSPATH", EXPERIMENT_ROOT_ABSPATH)

DB_DEFAULT_DB_NAME = 'rl.sqlite3'

EXPERIMENT_RESULTS_DIRECTORY_ABSPATH = create_path(EXPERIMENT_ROOT_ABSPATH, 'exp_results/')
EXPERIMENT_DATAFRAMES_DIRECTORY_ABSPATH = create_path(EXPERIMENT_RESULTS_DIRECTORY_ABSPATH, 'dataframes/')
EXPERIMENT_DATABASE_DIRECTORY_ABSPATH = create_path(EXPERIMENT_RESULTS_DIRECTORY_ABSPATH, 'databases/')
EXPERIMENT_DATABASE_OBJECT_ABSPATH = join(EXPERIMENT_DATABASE_DIRECTORY_ABSPATH, DB_DEFAULT_DB_NAME)

EXPERIMENT_LOGS_DIRECTORY_ABSPATH = create_path(EXPERIMENT_ROOT_ABSPATH, 'logs/')
EXPERIMENT_LOG_IMAGES_DIRECTORY_ABSPATH = create_path(EXPERIMENT_LOGS_DIRECTORY_ABSPATH, 'images/')

EXPERIMENT_REPORTS_DIRECTORY_ABSPATH = create_path(EXPERIMENT_ROOT_ABSPATH, 'reports/')
EXPERIMENT_EXP_INPUTS_DIRECTORY_ABSPATH = create_path(EXPERIMENT_ROOT_ABSPATH, 'input_params/')
EXPERIMENT_PERFMONITORING_DIRECTORY_ABSPATH = create_path(EXPERIMENT_ROOT_ABSPATH, 'performance_monitoring/')


