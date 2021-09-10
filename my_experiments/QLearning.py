import numpy as np

from rl.core.agents import Agent
from rl.core.envs import wrap_env

from my_experiments.misc import MapFloatToInteger

class TabularQLearningAgent(Agent):
    def __init__(self, points_per_dim):
        assert points_per_dim >= 2
        self.points_per_dim = points_per_dim
        self.q_table = None

    def set_env(self, env):
        print(env)
        wrapped_env = wrap_env(env)
        print(wrapped_env.info())
        self.state_low, self.state_high = wrapped_env.state_low, wrapped_env.state_high
        self.state_diff = self.state_high-self.state_low

        self.state_dims = wrapped_env.state_dims()
        print(self.state_low, self.state_high, self.state_diff, self.state_dims)

        assert wrapped_env.action_dims() == 1, 'QLearningAgent is not working for environments with action space with more than one dimensions.'

        if wrapped_env.is_action_space_discrete():
            n_action_points = wrapped_env.action_high[0]-wrapped_env.action_low[0]+1
            self.actions_mapping_f = lambda x: x
        else:
            n_action_points = self.points_per_dim
            mapper = MapFloatToInteger(low=wrapped_env.action_low[0],
                                       high=wrapped_env.action_high[0],
                                       n=n_action_points)
            self.actions_mapping_f = lambda x: mapper.map(x)

        print(n_action_points)
        self.q_table = np.random.normal(size=[self.points_per_dim]*self.state_dims+[n_action_points])
        print(self.q_table)

        self.states_mapping_f_list = []
        for dim_range in wrapped_env.state_limits().T:
            low, high = dim_range
            self.states_mapping_f_list.append(MapFloatToInteger(low, high, self.points_per_dim))

        # print(wrapped_env.state_limits())
        # for i in np.linspace(-1.2, 0.6, 10):
        #     for j in np.linspace(-.07, .07, 10):
        #         # s = wrapped_env.random_state()
        #         s = [i, j]
        #         print(s, self.__state_index(s), self.__q_of_state(s), self.act(s))
        # # s = [-1.2, -0.07]
        # # print(s, self.__q_of_state(s))
        # # s = [0.6, 0.07]
        # # print(s, self.__q_of_state(s))
        # # s = [-1.2, 0.07]
        # # print(s, self.__q_of_state(s))
        # # s = [0.6, -0.07]
        # # print(s, self.__q_of_state(s))
        # # exit()
        pass

    def __state_index(self, state):
        return tuple([self.states_mapping_f_list[i].map(s) for i, s in enumerate(state)])

    def __q_of_state(self, state):
        index = self.__state_index(state)
        res = self.q_table[index]
        return res

    def act(self, state):
        return [np.argmax(self.__q_of_state(state))]

import gym
from rl.core import engine
env = gym.make('MountainCarContinuous-v0')
# env = gym.make('MountainCar-v0')
agent = TabularQLearningAgent(4)
engine.run_episodes(env, agent, 2)