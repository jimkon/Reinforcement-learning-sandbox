import numpy as np

from rl.core.envs import wrap_env


class Agent:

    def set_env(self, env):
        pass

    def act(self, state):
        raise NotImplementedError

    def observe(self, state, action, reward, next_state, done):
        pass

    def name(self):
        return 'default_agent'


class QLearningAgent(Agent):
    def __init__(self, n_dims):
        self.n_dims = n_dims
        self.q_table = None

    def set_env(self, env):
        wrapped_env = wrap_env(env)
        pass

    def act(self, state):
        return np.random.randint(0, self.n_actions)

import gym
env = gym.make('MountainCar-v0')
print(env.)