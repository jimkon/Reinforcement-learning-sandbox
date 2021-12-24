import datetime

import gym

from rl.core.engine import run_episodes

from rl.agents.QLearning import TabularQLearningAgent


def experiment_args():
    resolution = 25

    time_signature = str(datetime.datetime.now()).replace('-', '').replace(':', '').replace(' ', '')

    experiment_name = f'qlearning_tab{resolution}_pend_{time_signature}'

    env = gym.make('Pendulum-v0')

    agent = TabularQLearningAgent(resolution, epsilon=.0)

    res = {
        'env': env,
        'agent': agent,
        'n_episodes': 2000,
        'experiment_name': experiment_name,

    }

    return res

    # from overall_results import plot_db_experiment
    # plot_db_experiment(experiment_name, 'Pendulum_v0', save_graph=False)
