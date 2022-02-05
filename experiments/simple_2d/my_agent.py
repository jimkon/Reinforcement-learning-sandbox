from functools import cached_property, lru_cache

import numpy as np

from rl.src.core.agents import AbstractAgent
from experiments.simple_2d.simple_env import *
from experiments.simple_2d.np_cache import np_cache
from experiments.simple_2d.alphastar import solve, path
from rl.src.core.logging import Logger

logger = Logger('my_agent')


class MyAgent_Abstract_SE_HC(AbstractAgent):

    # @np_cache()
    def actions(self):
        range_1d = list(range(MIN_ACTION, MAX_ACTION+1))

        actions = np.array([[a1, a2] for a1 in range_1d for a2 in range_1d])

        return actions

    def transition(self, state, action):
        next_state = np.clip(state + action,
                             a_min=[0, 0],
                             a_max=[DEFAULT_MAP_WIDTH - 1, DEFAULT_MAP_HEIGHT - 1])

        return next_state

    def transitions(self, state):
        next_states = [self.transition(state, a) for a in self.actions()]
        return next_states

    @logger.log_func_call('agent')
    def reward(self, state):
        state_x, state_y = state
        reward = DEFAULT_MAP[state_x][state_y]
        return reward

    def step_distance(self, state_a, state_b):
        return np.max(np.abs(state_a-state_b))

    def euclidean_distance(self, state_a, state_b):
        return np.sqrt(np.sum(np.square(state_b-state_a)))

    # @np_cache()
    def max_reward_state(self):
        logger.log("test message in function")
        exit()
        map = DEFAULT_MAP
        max_1d = np.max(map, axis=0)
        argmax_x = np.argmax(max_1d)
        argmax_y = np.argmax(map[:, argmax_x])
        return np.array([argmax_x, argmax_y])

    # @np_cache()
    def shortest_path_actions(self, state, to_state):
        delta = to_state-state
        actions = []
        for i in range(self.step_distance(state, to_state)):
            action = np.clip(delta,
                             a_min=MIN_ACTION,
                             a_max=MAX_ACTION)
            delta -= action
            actions.append(action)
        return np.array(actions)

    def best_path_actions(self, state_a, state_b):
        start_node, n, open_set, close_set = solve(start_state=state_a,
                                                   goal_state=state_b,
                                                   h_func=lambda s_a, s_b: self.step_distance(s_a, s_b),
                                                   next_actions_func=lambda s: self.actions(),
                                                   next_states_func=lambda s, a: self.transitions(s),
                                                   g_func=lambda s1, s2: self.reward(s2))

        self.path_states, self.path_actions = path(start_node)
        return self.path_actions


class MyAgent_Greedy_SE_HC(MyAgent_Abstract_SE_HC):

    def act(self, state):
        __min_reward = -np.Inf
        __best_action = None
        for action in self.actions():
            next_state = self.transition(state, action)
            reward = self.reward(next_state)
            if reward >= __min_reward:
                __min_reward = reward
                __best_action = action
        return __best_action

    def name(self):
        return 'my_agent_greedy_hardcoded'


class MyAgent_ShortestPath_SE_HC(MyAgent_Abstract_SE_HC):
    #
    # def __init__(self):
    #     self.h_func = lambda cs, gs: np.max(np.abs(cs-gs))
    #     self.next_actions_func = lambda s: self.actions(s)
    #     self.next_states_func = lambda s: self.transitions(s)
    #     self.g_func = lambda s1, s2: 1
    #
    #     self.last_goal_state = None
    #     self.path_states = None
    #     self.path_actions = None

    def act(self, state):
        current_goal_state = self.max_reward_state()
        actions = self.best_path_actions(state, current_goal_state)
        return actions[0]
        # if self.path_states and\
        #     current_goal_state == self.last_goal_state and\
        #     state in self.path_states:
        #
        #     for i, s in enumerate(self.path_states):
        #         if state == s:
        #             return self.path_actions[i]
        # else:
        #     self.last_goal_state = current_goal_state
        #     self.best_path_actions(state, self.last_goal_state)

    def name(self):
        return 'my_agent_shortest_path_to_global_max_hardcoded'


if __name__ == "__main__":
    a = MyAgent_Greedy_SE_HC()
    print(a.shortest_path_actions(np.array([50, 50]), np.array([51, 51])))

