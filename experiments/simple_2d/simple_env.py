import time

import numpy as np
import cv2
import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise

from rl.src.core.envs import AbstractEnv
from rl.src.core.logging import Logger


def perlin_map(width=100, height=100, octaves=3, seed=6):
    noise = PerlinNoise(octaves=octaves, seed=seed)
    xpix, ypix = width, height
    pic = np.array([[noise([i / xpix, j / ypix]) for j in range(xpix)] for i in range(ypix)])
    pic -= pic.min()
    pic /= pic.max()

    return np.array(pic)


DEFAULT_MAP_WIDTH = 100
DEFAULT_MAP_HEIGHT = 100
DEFAULT_MAP = perlin_map(width=DEFAULT_MAP_WIDTH, height=DEFAULT_MAP_HEIGHT)

MIN_ACTION = -1
MAX_ACTION = 1
STEPS_PER_EPISODE = 100
STARTING_X = 50
STARTING_Y = 50

logger = Logger('simple_env')


class SimpleEnv(AbstractEnv):

    def __init__(self):
        self.width, self.height = DEFAULT_MAP_WIDTH, DEFAULT_MAP_HEIGHT
        self.map = DEFAULT_MAP
        self.min_action, self.max_action = MIN_ACTION, MAX_ACTION
        self.steps_per_episode = STEPS_PER_EPISODE

        self.x, self.y = -1, -1
        self.step_count = -1

        self.track_x, self.track_y = [], []

        plt.ion()

    @logger.log_func_call()
    def reset(self):
        self.x, self.y = STARTING_X, STARTING_Y
        self.step_count = -1

        self.track_x, self.track_y = [self.x], [self.y]

        state = np.array([self.x, self.y])
        return state

    def step(self, action):
        action = np.clip(np.round(action),
                         a_min=self.min_action,
                         a_max=self.max_action)

        state = np.array([self.x, self.y])

        next_state = np.clip(state+action,
                             a_min=[0, 0],
                             a_max=[self.width-1, self.height-1])
        self.x, self.y = next_state
        self.track_x.append(self.x), self.track_y.append(self.y)

        reward = self.map[self.x][self.y]

        self.step_count += 1

        done = self.step_count == self.steps_per_episode
        return next_state, reward, done, None

    def render(self):
        plt.imshow(self.map)
        plt.tight_layout()
        if len(self.track_x) >= 4:
            c1 = np.linspace(.2, 1, len(self.track_x))
            c = np.array([c1, c1, c1]).T
            plt.scatter(self.track_x,
                        self.track_y,
                        c=c,
                        marker='o')
        plt.plot(self.x, self.y, 'ro')
        plt.plot(STARTING_X, STARTING_Y, 'mx')
        plt.draw()
        plt.pause(0.00001)
        plt.clf()

    def __repr__(self):
        return "SimpleEnv"

#
# if __name__ == "__main__":
#     env = SimpleEnv()
#     env.reset()
#
#     while True:
#         env.render()
#         print("key")


