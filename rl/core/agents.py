import numpy as np


class Agent:

    def set_env(self, env):
        pass

    def act(self, state):
        raise NotImplementedError

    def observe(self, state, action, reward, next_state, done):
        pass

    def name(self):
        return 'default_agent'


class RandomAgent(Agent):
    def __init__(self, n_actions):
        # self.states_dims = states_dims
        self.n_actions = n_actions

        # self.q_table = np.random.random((self.n_actions, *self.states_dims))

    def act(self, state):
        return np.random.randint(0, self.n_actions)

