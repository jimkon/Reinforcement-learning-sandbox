import os

PROJECT_DIRECTORY = os.path.dirname(os.path.dirname(__file__))
print("PROJECT_DIRECTORY", PROJECT_DIRECTORY)

STORE_COMPRESSED_DATA = False

DEFAULT_STORE_RESULTS_OBJECT = 'database'

DEFAULT_STORE_DATAFRAMES_DIRECTORY_PATH = os.path.normpath(os.path.join(PROJECT_DIRECTORY, '../files/results/dataframes/'))
DEFAULT_STORE_DATABASES_DIRECTORY_PATH = os.path.normpath(os.path.join(PROJECT_DIRECTORY, '../files/results/databases/'))
DEFAULT_STORE_DATABASE_OBJECT_PATH = os.path.normpath(os.path.join(DEFAULT_STORE_DATABASES_DIRECTORY_PATH, 'rl.db'))

DB_VERBOSITY = 1
DB_DEFAULT_DB_NAME = 'rl'
