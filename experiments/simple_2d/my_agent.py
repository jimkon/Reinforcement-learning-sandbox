from rl.src.core.agents import AbstractAgent
from experiments.simple_2d.simple_env import *
from experiments.simple_2d.np_cache import np_cache
from experiments.simple_2d.alphastar import solve, path
from rl.src.core.logging import Logger

logger = Logger('my_agent')


def plot_path(path):
    start_state, end_state = path[0], path[-1]
    plt.figure()
    plt.imshow(DEFAULT_MAP)

    plt.plot(path[:, 0], path[:, 1], 'r-')
    plt.plot([start_state[0]], [start_state[1]], 'mo')
    plt.plot([end_state[0]], [end_state[1]], 'rv')
    plt.tight_layout()
    logger.log_plt(title='agent_action')


def state_plus_actions(state, actions):
    new_state = state
    path = [new_state]
    for action in actions:
        new_state = new_state+action
        path.append(new_state)

    return np.array(path)


def find_state_in_path(state, path):
    for i, s in enumerate(path):
        if np.array_equal(state, s):
            return i
    return -1


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

        if len(actions) == 0:
            return np.array([0, 0])

        actions = np.array(actions)
        return actions

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
    def __init__(self):
        self.path = None
        self.actions = None
        self.current_goal = self.max_reward_state()

    def act(self, state):
        if self.path is not None:
            ind = find_state_in_path(state, self.path)
            if ind < 0:
                self.path = None
                self.actions = None
            elif ind >= len(self.actions):
                return [0, 0]
            else:
                return self.actions[ind]

        if self.path is None:
            self.actions = self.shortest_path_actions(state, self.current_goal)
            self.path = state_plus_actions(state, self.actions)
            plot_path(self.path)
            logger.log(f"my agent: act: Regenerate path from {state} to {self.current_goal}")

        return self.actions[0]

    def name(self):
        return 'my_agent_shortest_path_to_global_max_hardcoded'

