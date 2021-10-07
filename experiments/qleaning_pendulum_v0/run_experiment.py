import numpy as np

from QLearning import TabularQLearningAgent

if __name__=="__main__":
    import gym

    class RewardWrapper(gym.RewardWrapper):
        def __init__(self, env):
            super().__init__(env)

        def step(self, action):
            next_state, reward, done, _ = super().step(action)
            x, v = next_state
            if done and x >= .5:
                reward = 100
            else:
                reward = abs(x+0.5)
            return next_state, reward, done, _

        def reward(self, rew):
            return 0

    from rl.core import engine
    # env = gym.make('MountainCarContinuous-v0')
    # env = gym.make('MountainCar-v0')
    # env = RewardWrapper(gym.make('MountainCar-v0'))
    env = gym.make('Pendulum-v0')
    agent = TabularQLearningAgent(10, epsilon=.0)
    engine.run_episodes(env,
                        agent,
                        2000,
                        store_results='dataframe',
                        experiment_name='pend',
                        verbosity='episode',
                        render=False)
    print(np.moveaxis(agent.q_table, -1, 0))