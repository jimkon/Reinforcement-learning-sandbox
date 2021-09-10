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



