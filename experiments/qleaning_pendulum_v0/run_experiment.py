import numpy as np

from QLearning import TabularQLearningAgent

if __name__=="__main__":
    import gym

    from rl.core.engine import run_episodes

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
