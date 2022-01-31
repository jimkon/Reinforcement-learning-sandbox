from rl.src.core.engine import run_episodes

from experiments.simple_2d.simple_env import SimpleEnv
from experiments.simple_2d.random_walk_agent import RandomWalkAgent


def run_experiment():
    agent = RandomWalkAgent()
    env = SimpleEnv()
    experiment_name = 'simple_experiment_test'

    # run_and_store_episodes(env, agent, 3, experiment_name, store_results_func='database', verbosity='step')
    run_episodes(env, agent, 3, verbosity='step', render=False)


if __name__ == "__main__":
    run_experiment()
