import numpy as np

from rl.src.core.agents import AbstractAgent
from experiments.simple_2d.simple_env import *
from experiments.simple_2d.np_cache import np_cache
from experiments.simple_2d.alphastar import solve, path
from rl.src.core.logging import Logger

logger = Logger('my_agent')


def plot_path(path):
    img = np.dstack(DEFAULT_MAP.copy())
    cv2.polylines(img, [path], False, (0, 255, 255))
    cv2.imshow('plotting the path', img)
    cv2.waitKey(0)



def state_plus_actions(state, actions):
    new_state = state
    path = [new_state]
    for action in actions:
        new_state = new_state+action
        path.append(new_state)

    return np.array(path)


def find_state_in_path(state, path):
    if state is None or path is None:
        return -1

    for i, s in enumerate(path):
        if np.array_equal(state, s):
            return i
    return -1


def states_equal(state_1, state_2):
    if state_1 is None or state_2 is None:
        return False
    return np.array_equal(state_1, state_2)


class MyAgent_Abstract_SE_POC(AbstractAgent):

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
        actions = self.actions()
        next_states = np.array([self.transition(state, a) for a in actions])
        return next_states, actions

    def reward(self, state):
        state_x, state_y = state
        reward = DEFAULT_MAP[state_x][state_y]
        return reward

    def step_distance(self, state_a, state_b):
        return np.max(np.abs(state_a-state_b))

    def euclidean_distance(self, state_a, state_b):
        return np.sqrt(np.sum(np.square(state_b-state_a)))


class MyAgent_Greedy_SE_POC(MyAgent_Abstract_SE_POC):

    def act(self, state):
        m = DEFAULT_MAP
        next_states, actions = self.transitions(state)
        rewards = [self.reward(next_state) for next_state in next_states]
        index = np.argmax(rewards)
        res_action = actions[index]
        return res_action

    def name(self):
        return 'my_greedy_POC_agent'


class MyAgent_Abstract_PathPlanning_POC(MyAgent_Abstract_SE_POC):

    def __init__(self):
        self.__path = None
        self.__actions = None
        # self.current_goal = None

    def act(self, state):
        action = self.follow_the_path(state)
        return action

    def follow_the_path(self, current_state):
        target_state = self.target_state()
        if self.__path is None or self.__actions is None:
            logger.log("Calculating path. Reason: no path found.")
            self.__path, self.__actions = self.calculate_path_and_actions(current_state, target_state)

        path_last_state, path_first_state = self.__path[-1], self.__path[0]

        if not states_equal(target_state, path_last_state) or not states_equal(current_state, path_first_state):
            logger.log(f"Calculating path. Reason: Path failed. new target state:{not states_equal(target_state, path_last_state)}, current state missed:{not states_equal(current_state, path_first_state)}")
            self.__path, self.__actions = self.calculate_path_and_actions(current_state, target_state)

        result_action = self.__actions[-1]
        self.__path, self.__actions = self.__path[:-1], self.__actions[:-1]
        return result_action

    @logger.log_func_call('agent')
    def calculate_path_and_actions(self, state_a, state_b):
        raise NotImplementedError

    @logger.log_func_call('agent')
    def target_state(self):
        raise NotImplementedError

    @logger.log_func_call('agent')
    def max_reward_state(self):
        map = DEFAULT_MAP
        max_1d = np.max(map, axis=0)
        argmax_x = np.argmax(max_1d)
        argmax_y = np.argmax(map[:, argmax_x])
        return np.array([argmax_x, argmax_y])


class MyAgent_ShortestPath_SE_POC(MyAgent_Abstract_PathPlanning_POC):

    def calculate_path_and_actions(self, state_a, state_b):
        paths, actions = self.shortest_path_actions(state_a, state_b)
        return paths, actions

    def name(self):
        return 'my_shortest_path_to_max_reward_state_POC_agent'

    def shortest_path_actions(self, state_a, state_b):
        if states_equal(state_a, state_b):
            return np.array([0, 0])

        delta = state_b - state_a
        cur_state = state_a
        states = [cur_state]
        actions = []
        for i in range(self.step_distance(state_a, state_b)):
            action = np.clip(delta,
                             a_min=MIN_ACTION,
                             a_max=MAX_ACTION)
            delta -= action
            actions.append(action)

            cur_state += action
            states.append(cur_state)

        return np.array(states), np.array(actions)


class MyAgent_BestPath_SE_POC(MyAgent_Abstract_PathPlanning_POC):

    def best_path_actions(self, state_a, state_b):
        start_node, n, open_set, close_set = solve(start_state=state_a,
                                                   goal_state=state_b,
                                                   h_func=lambda s_a, s_b: self.step_distance(s_a, s_b),
                                                   next_actions_func=lambda s: self.actions(),
                                                   next_states_func=lambda s, a: self.transitions(s),
                                                   g_func=lambda s1, s2: self.reward(s2))

        self.path_states, self.path_actions = path(start_node)
        return self.path_actions
