from rl.core.rl.engine import run_episodes
from rl.core.utilities.logging import save_loggers

from experiments.simple_2d.my_agent import *


def run_experiment():
    # agent = RandomWalkAgent()
    # agent = MyAgent_Greedy_SE_POC()
    # agent = MyAgent_ShortestPath_SE_POC()
    agent = MyAgent_BestPath_SE_POC()

    env = SimpleEnv()

    experiment_name = 'simple_experiment_test'
    # logger(experiment_name)
    # run_and_store_episodes(env, agent, 3, experiment_name, store_results_func='database', verbosity='step')
    run_episodes(env, agent, 1, verbosity='step', render=True)
    # logger.save()
    save_loggers()

if __name__ == "__main__":

    run_experiment()
