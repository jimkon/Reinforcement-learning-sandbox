from functools import cached_property, lru_cache

import numpy as np

from rl.src.core.agents import AbstractAgent
from experiments.simple_2d.simple_env import *
from experiments.simple_2d.np_cache import np_cache


class MyAgent_Abstract_SE_HC(AbstractAgent):

    def __init__(self):
        self.min_reward = DEFAULT_MAP.min()
        self.max_reward = DEFAULT_MAP.max()

    @np_cache()
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

    def reward(self, state):
        state_x, state_y = state
        reward = DEFAULT_MAP[state_x][state_y]
        return reward

    @np_cache()
    def goal_state(self):
        print('goal_state')
        map = DEFAULT_MAP
        max_1d = np.max(map, axis=0)
        argmax_x = np.argmax(max_1d)
        argmax_y = np.argmax(map[:, argmax_x])
        return np.array([argmax_x, argmax_y])



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

    def act(self, state):
        goal_state = self.goal_state()
        __min_distance = np.inf
        __best_action = None
        for action in self.actions():
            next_state = self.transition(state, action)
            dist = np.sqrt(np.sum(np.square(goal_state-next_state)))
            if dist <= __min_distance:
                __min_distance = dist
                __best_action = action
            pass
        return __best_action

    def name(self):
        return 'my_agent_shortest_path_to_global_max_hardcoded'





# if __name__ == "__main__":
#     a = MyAgent_Greedy_SE_HC()

