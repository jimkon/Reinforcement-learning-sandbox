from os.path import join
from configparser import ConfigParser


from rl.src.core.logging import log

PROJECT_ROOT_DIRECTORY = "Reinforcement-learning-sandbox"
PROJECT_ROOT_ABSPATH = join(__file__.split(PROJECT_ROOT_DIRECTORY)[0], PROJECT_ROOT_DIRECTORY)
log("PROJECT_DIRECTORY", PROJECT_ROOT_ABSPATH)


RUN_CONFIGS_FILENAME = 'run_config.ini'
RUN_CONFIGS_ABSPATH = join(PROJECT_ROOT_ABSPATH, RUN_CONFIGS_FILENAME)
print(RUN_CONFIGS_ABSPATH)

__configs = ConfigParser()
__configs.read(RUN_CONFIGS_ABSPATH)

EXPERIMENT_ROOT_DIRECTORY = join(__configs['DEFAULTS']['experiments_dir'],
                                 __configs['EXPERIMENT']['module'])
EXPERIMENT_ROOT_ABSPATH = join(PROJECT_ROOT_ABSPATH, EXPERIMENT_ROOT_DIRECTORY)

STORE_COMPRESSED_DATA = False

DEFAULT_STORE_RESULTS_OBJECT = 'database'

DEFAULT_STORE_DATAFRAMES_DIRECTORY_PATH = 'files/results/dataframes/'
DEFAULT_STORE_DATABASES_DIRECTORY_PATH = 'files/results/databases/'
DEFAULT_STORE_DATABASE_OBJECT_PATH = join(DEFAULT_STORE_DATABASES_DIRECTORY_PATH, 'rl.db')

DB_VERBOSITY = 1
DB_DEFAULT_DB_NAME = 'rl'

TIMESTAMP_STRING_FORMAT = "%m-%d-%Y--%H-%M-%S"


