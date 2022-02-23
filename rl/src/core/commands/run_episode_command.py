from rl.src.core.platform.command import AbstractCommand
from rl.src.core.utilities.profiling import cprofile
from rl.src.core.logging import Logger
from rl.src.core.rl.agents import get_agent
from rl.src.core.rl.envs import get_env
from rl.src.core.rl.engine import run_episodes


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
        self.__n_repeat = run_params['n_repeat'] if 'n_repeat' in run_params.keys() else 1

    @cprofile
    @logger.log_func_call()
    def run(self):
        self.res_list = []
        for i in range(self.__n_repeat):
            res = run_episodes(self.__env,
                                self.__agent,
                                self.__run_kwargs['n_episodes'],
                                storage_dict=None,
                                #storage_dict=res_dict,
                                render=False
                                )
            self.res_list.append(res)

    def output(self):
        for d in self.res_list:
            self.write_to_file(d)




