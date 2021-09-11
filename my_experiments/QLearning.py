import numpy as np

from rl.core.agents import Agent
from rl.core.envs import wrap_env

from my_experiments.misc import MapFloatToInteger


class TabularQLearningAgent(Agent):
    def __init__(self, points_per_dim, a=0.9, gamma=0.9, epsilon=1):
        assert points_per_dim >= 2
        self.points_per_dim = points_per_dim
        self.q_table = None

        self.learning_rate = a
        self.discount_rate = gamma
        self.epsilon = epsilon

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
        self.q_table = np.ones(shape=[self.points_per_dim]*self.state_dims+[n_action_points])*0.8
        print(np.moveaxis(self.q_table, -1, 0))

        self.states_mapping_f_list = []
        for dim_range in self.wrapped_env.state_limits().T:
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
        if np.random.uniform() < self.epsilon:
            # action = self.wrapped_env.random_action()
            action_i = 0 if state[1] < 0 else 2
        else:
            action_i = np.argmax(self.__q_of_state(state))

        if not self.is_action_space_discrete:
            action = [self.action_mapper.map_out(action_i)]

        else:
            action = action_i

        return action

    def observe(self, state, action, reward, next_state, done):
        if not self.is_action_space_discrete:
            action_i = int(self.action_mapper.map_in(action[0]))
        else:
            action_i = action

        if done:
            new_Q_s_a = self.discount_rate * reward
        else:
            Q_s = self.__q_of_state(state)
            current_Q_s_a = Q_s[action_i]
            Q_sn = self.__q_of_state(next_state)
            max_Q_sn = np.max(Q_sn)

            new_Q_s_a = current_Q_s_a + self.learning_rate * (reward+self.discount_rate*max_Q_sn-current_Q_s_a)

        index = self.__state_index(state)
        self.q_table[index][action_i] = new_Q_s_a

        return

    def name(self):
        return 'tabular_Q_learning'


if __name__=="__main__":
    import gym
    from rl.core import engine
    env = gym.make('MountainCarContinuous-v0')
    # env = gym.make('MountainCar-v0')
    agent = TabularQLearningAgent(6)
    engine.run_episodes(env, agent, 1000, verbosity='episode', render=False)
    print(np.moveaxis(agent.q_table, -1, 0))
