from rl.src.core.engine import run_episodes
from rl.src.core.logging import logger

from experiments.simple_2d.simple_env import SimpleEnv
from experiments.simple_2d.random_walk_agent import RandomWalkAgent
from experiments.simple_2d.my_agent import *
from experiments.simple_2d.my_agent import logger as agent_logger


def run_experiment():
    # agent = RandomWalkAgent()
    agent = MyAgent_Greedy_SE_HC()
    # agent = MyAgent_ShortestPath_SE_HC()
    env = SimpleEnv()
    experiment_name = 'simple_experiment_test'
    # logger(experiment_name)
    # run_and_store_episodes(env, agent, 3, experiment_name, store_results_func='database', verbosity='step')
    run_episodes(env, agent, 1, verbosity='step', render=True)
    # logger.save()
    agent_logger.save()

if __name__ == "__main__":
    run_experiment()
