import os

PROJECT_DIRECTORY = os.path.dirname(os.path.dirname(__file__))
print("PROJECT_DIRECTORY", PROJECT_DIRECTORY)

STORE_COMPRESSED_DATA = False

DEFAULT_STORE_RESULTS_OBJECT = 'dataframe'

DEFAULT_STORE_DATAFRAMES_DIRECTORY_PATH = os.path.normpath(os.path.join(PROJECT_DIRECTORY, '../files/results/dataframes/'))
print("DEFAULT_STORE_DATAFRAMES_DIRECTORY_PATH", DEFAULT_STORE_DATAFRAMES_DIRECTORY_PATH)

DB_VERBOSITY = 1
DB_DEFAULT_DB_NAME = 'rl'
