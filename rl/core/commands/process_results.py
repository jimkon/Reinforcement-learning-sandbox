from rl.core.configs.path_confgis import EXPERIMENT_DATAFRAMES_DIRECTORY_ABSPATH,\
    EXPERIMENT_DATABASE_OBJECT_ABSPATH
from rl.core.configs.storage_configs import DB_EXPERIMENT_TABLE_NAME_COL_EXPID
from rl.core.platform.command import AbstractCommand
from rl.core.storage.storage import compress_data_df
from rl.core.utilities.logging import Logger

# TODO
# process and transform results
# store results in db
from rl.core.utilities.profiling import cprofile


class ProcessResultsCommand(AbstractCommand):

    alias = 'pr'
    logger = Logger(f"Command {alias}")

    def __init__(self):
        super().__init__(input_dir=EXPERIMENT_DATAFRAMES_DIRECTORY_ABSPATH,
                         output_dir=EXPERIMENT_DATABASE_OBJECT_ABSPATH)

    def input(self):
        files = self.read_file()
        self._file = files[0]
        self._input_df = self.read_file(self._file)

    @cprofile
    @logger.log_func_call()
    def run(self):
        transformed_df = compress_data_df(self._input_df)
        transformed_df[DB_EXPERIMENT_TABLE_NAME_COL_EXPID] = self._file
        pass

    def output(self):
        pass
