from os.path import join
from configparser import ConfigParser


# PROJECT_ROOT_DIRECTORY = "Reinforcement-learning-sandbox"
# PROJECT_ROOT_ABSPATH = join(__file__.split(PROJECT_ROOT_DIRECTORY)[0], PROJECT_ROOT_DIRECTORY)
# print("PROJECT_DIRECTORY", PROJECT_ROOT_ABSPATH)
#
#
# RUN_CONFIGS_FILENAME = 'run_config.ini'
# RUN_CONFIGS_ABSPATH = join(PROJECT_ROOT_ABSPATH, RUN_CONFIGS_FILENAME)
# print("RUN_CONFIGS_ABSPATH", RUN_CONFIGS_ABSPATH)
#
# __configs = ConfigParser()
# __configs.read(RUN_CONFIGS_ABSPATH)
#
# EXPERIMENT_ROOT_DIRECTORY = join(__configs['DEFAULTS']['experiments_dir'],
#                                  __configs['EXPERIMENT']['module'])
# EXPERIMENT_ROOT_ABSPATH = join(PROJECT_ROOT_ABSPATH, EXPERIMENT_ROOT_DIRECTORY)
# print("EXPERIMENT_ROOT_ABSPATH", EXPERIMENT_ROOT_ABSPATH)

STORE_COMPRESSED_DATA = False
# DB_DEFAULT_DB_NAME = 'rl.sqlite3'
#
# DEFAULT_STORE_FILES_DIRECTORY_PATH = 'files/'
# DEFAULT_STORE_RESULTS_DIRECTORY_PATH = join(DEFAULT_STORE_FILES_DIRECTORY_PATH, 'results/')
# DEFAULT_STORE_DATAFRAMES_DIRECTORY_PATH = join(DEFAULT_STORE_RESULTS_DIRECTORY_PATH, 'dataframes/')
# DEFAULT_STORE_DATABASE_DIRECTORY_PATH = join(DEFAULT_STORE_RESULTS_DIRECTORY_PATH, 'databases/')
# DEFAULT_STORE_DATABASE_OBJECT_PATH = join(DEFAULT_STORE_DATABASE_DIRECTORY_PATH, DB_DEFAULT_DB_NAME)
# DEFAULT_STORE_LOGS_DIRECTORY_PATH = join(DEFAULT_STORE_FILES_DIRECTORY_PATH, 'logs/')
# DEFAULT_STORE_INPUTS_OUTPUTS_DIRECTORY_PATH = join(DEFAULT_STORE_FILES_DIRECTORY_PATH, 'transient/')
# DEFAULT_STORE_PERFMONITORING_DIRECTORY_PATH = join(DEFAULT_STORE_LOGS_DIRECTORY_PATH, 'performance_monitoring/')
#
#
# EXPERIMENT_STORE_DATAFRAMES_DIRECTORY_ABSPATH = join(EXPERIMENT_ROOT_ABSPATH, DEFAULT_STORE_DATAFRAMES_DIRECTORY_PATH)
# EXPERIMENT_STORE_DATABASE_DIRECTORY_ABSPATH = join(EXPERIMENT_ROOT_ABSPATH, DEFAULT_STORE_DATABASE_DIRECTORY_PATH)
# EXPERIMENT_STORE_DATABASE_OBJECT_ABSPATH = join(EXPERIMENT_STORE_DATABASE_DIRECTORY_ABSPATH, DB_DEFAULT_DB_NAME)
# EXPERIMENT_STORE_LOGS_DIRECTORY_ABSPATH = join(EXPERIMENT_ROOT_ABSPATH, DEFAULT_STORE_LOGS_DIRECTORY_PATH)
# EXPERIMENT_STORE_INPUTS_OUTPUTS_DIRECTORY_ABSPATH = join(EXPERIMENT_ROOT_ABSPATH, DEFAULT_STORE_INPUTS_OUTPUTS_DIRECTORY_PATH)
# EXPERIMENT_STORE_PERFMONITORING_DIRECTORY_ABSPATH = join(EXPERIMENT_ROOT_ABSPATH, DEFAULT_STORE_PERFMONITORING_DIRECTORY_PATH)


TIMESTAMP_STRING_FORMAT = "%Y-%d-%m_%H-%M-%S"
TIMESTAMP_LONG_STRING_FORMAT = TIMESTAMP_STRING_FORMAT+"_%f"

CPROFILE_COMMAND_EXECUTION_FLAG = True


