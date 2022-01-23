import os.path
from os.path import dirname, join, normpath, sep

from src.rl.core.configs.run import PROJECT_ROOT_ABSPATH,\
    DEFAULT_STORE_DATAFRAMES_DIRECTORY_PATH,\
    DEFAULT_STORE_DATABASES_DIRECTORY_PATH,\
    DEFAULT_STORE_DATABASE_OBJECT_PATH

DEFAULT_EXPERIMENT_PATH = 'experiments/test/experiment/'
EXPERIMENT_PATH = DEFAULT_EXPERIMENT_PATH

STORE_DATAFRAMES_DIRECTORY_ABSPATH = join(PROJECT_ROOT_ABSPATH,
                                          EXPERIMENT_PATH,
                                          DEFAULT_STORE_DATAFRAMES_DIRECTORY_PATH)
STORE_DATABASES_DIRECTORY_ABSPATH = join(PROJECT_ROOT_ABSPATH,
                                          EXPERIMENT_PATH,
                                          DEFAULT_STORE_DATABASES_DIRECTORY_PATH)
STORE_DATABASE_OBJECT_ABSPATH = join(PROJECT_ROOT_ABSPATH,
                                          EXPERIMENT_PATH,
                                          DEFAULT_STORE_DATABASE_OBJECT_PATH)
print(STORE_DATABASE_OBJECT_ABSPATH)
exit()


