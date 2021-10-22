import gym

from rl.core.engine import run_episodes
from QLearning import TabularQLearningAgent

if __name__ == "__main__":
    env = gym.make('Pendulum-v0')
    agent = TabularQLearningAgent(10, epsilon=.0)
    run_episodes(env,
                 agent,
                 2000,
                 store_results='database',
                 experiment_name='qlearning_tab20_pend',
                 verbosity='episode',
                 # log_frequency=100,
                 render=False)
