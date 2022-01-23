import numpy as np

from src.rl.core.agents import Agent
from src.rl.core.envs import wrap_env

from experiments.qlearning_pendulum_v0.src.misc import MapFloatToInteger


class TabularQLearningAgent(Agent):
    def __init__(self, points_per_dim, a=0.9, gamma=0.9, epsilon=.2):
        assert points_per_dim >= 2
        self.points_per_dim = points_per_dim
        self.q_table = None

        self.learning_rate = a
        self.discount_rate = gamma
        self.epsilon = epsilon

        self.wrapped_env = None
        self.state_low, self.state_high = None, None
        self.state_diff = None
        self.state_dims = None
        self.is_action_space_discrete = None
        self.action_mapper, self.actions_mapping_f = None, None
        self.states_mapping_f_list = None

    def set_env(self, env):
        print(env)
        self.wrapped_env = wrap_env(env)
        print(self.wrapped_env.info())
        self.state_low, self.state_high = self.wrapped_env.state_low, self.wrapped_env.state_high
        self.state_diff = self.state_high-self.state_low

        self.state_dims = self.wrapped_env.state_dims()
        print(self.state_low, self.state_high, self.state_diff, self.state_dims)

        self.is_action_space_discrete = self.wrapped_env.is_action_space_discrete()

        assert self.wrapped_env.action_dims() == 1, 'QLearningAgent is not working for environments with action space with more than one dimensions.'
        self.action_mapper = None
        if self.is_action_space_discrete:
            n_action_points = self.wrapped_env.action_high[0]-self.wrapped_env.action_low[0]+1
            self.actions_mapping_f = lambda x: x
        else:
            n_action_points = self.points_per_dim
            self.action_mapper = MapFloatToInteger(low=self.wrapped_env.action_low[0],
                                       high=self.wrapped_env.action_high[0],
                                       n=n_action_points)
            self.actions_mapping_f = lambda x: self.action_mapper.map(x)

        print(n_action_points)
        self.q_table = np.ones(shape=[self.points_per_dim]*self.state_dims+[n_action_points])*2

        self.states_mapping_f_list = []
        for dim_range in self.wrapped_env.state_limits().T:
            low, high = dim_range
            self.states_mapping_f_list.append(MapFloatToInteger(low, high, self.points_per_dim))

    def __state_index(self, state):
        return tuple([self.states_mapping_f_list[i].map(s) for i, s in enumerate(state)])

    def __q_of_state(self, state):
        index = self.__state_index(state)
        res = self.q_table[index]
        return res

    def act(self, state):
        if np.random.uniform() < self.epsilon:
            action = self.wrapped_env.random_action()
            return action
        else:
            action_i = np.argmax(self.__q_of_state(state))

        if self.is_action_space_discrete:
            action = action_i

        else:
            action = [self.action_mapper.reverse(action_i)]

        return action

    def observe(self, state, action, reward, next_state, done):
        if not self.is_action_space_discrete:
            action_i = int(self.action_mapper.map(action[0]))
        else:
            action_i = action

        if done:
            new_Q_s_a = self.discount_rate * reward
        else:
            Q_s = self.__q_of_state(state)
            current_Q_s_a = Q_s[action_i]
            Q_sn = self.__q_of_state(next_state)
            max_Q_sn = np.max(Q_sn)
            td = reward+self.discount_rate*max_Q_sn-current_Q_s_a
            new_Q_s_a = current_Q_s_a + self.learning_rate * td

        index = self.__state_index(state)
        self.q_table[index][action_i] = new_Q_s_a

        return

    def name(self):
        return f'Q_learning_tabular({self.points_per_dim})_v1'
