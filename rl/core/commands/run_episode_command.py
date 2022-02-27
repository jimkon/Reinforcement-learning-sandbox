import pandas as pd

from rl.core.platform.command import AbstractCommand
from rl.core.utilities.profiling import cprofile
from rl.core.utilities.logging import Logger
from rl.core.rl.agents import get_agent
from rl.core.rl.envs import get_env
from rl.core.rl.engine import run_episodes
from rl.core.utilities.timestamp import timestamp_unique_str
from rl.core.storage.storage import data_to_df

# TODO
# execute experiment
class RunEpisodeCommand(AbstractCommand):

    alias = 're'
    logger = Logger(f"Command {alias}")

    def input(self):
        run_params = self.read_file('run_parameters.json')
        self.__agent = get_agent(run_params['agent_name'])(**run_params['agent_params'])
        self.__env = get_env(run_params['env_name'])(**run_params['env_params'])
        self.__run_kwargs = run_params['run_kwargs']
        self.__n_repeat = int(run_params['n_repeat']) if 'n_repeat' in run_params.keys() else 1

    @cprofile
    @logger.log_func_call()
    def run(self):
        agent_id = self.__agent.name
        env_id = self.__env.name
        run_id = timestamp_unique_str()
        self.res_dict = {}
        for i in range(self.__n_repeat):
            exp_id = f"{agent_id}__{env_id}__{run_id}__{i}"
            res = run_episodes(self.__env,
                                self.__agent,
                                self.__run_kwargs['n_episodes'],
                                storage_dict=None,
                                #storage_dict=res_dict,
                                render=False
                                )
            self.res_dict[exp_id] = res

    def output(self):
        for key, data in self.res_dict.items():
            df = pd.DataFrame(data_to_df(data))
            self.write_to_file(df, f"{key}.csv")




