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

        max_1d = np.max(self.map, axis=0)
        self.argmax_y = np.argmax(max_1d)
        self.argmax_x = np.argmax(self.map[:, self.argmax_y])

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

        done = self.step_count == self.steps_per_episode-1
        return next_state, reward, done, None

    @logger.log_func_call('run_time')
    def render(self, width=500, height=500, fps=30):
        approx_wait_time = 1000//fps

        # m = self.map
        # m = np.square(self.map)
        m = np.round(self.map, 1)

        r_img = np.zeros(m.shape)
        g_img = m
        b_img = np.zeros(m.shape)

        for i, (x, y) in enumerate(zip(self.track_x, self.track_y)):
            i_ratio = i/100.
            r_img[x][y] = i_ratio*0.5
            g_img[x][y] = 1-i_ratio
            b_img[x][y] = 1

        r_img[STARTING_X][STARTING_Y] = 1
        g_img[STARTING_X][STARTING_Y] = 0
        b_img[STARTING_X][STARTING_Y] = 1

        r_img[self.x][self.y] = 1
        g_img[self.x][self.y] = 0
        b_img[self.x][self.y] = 0

        r_img[self.argmax_x][self.argmax_y] = 0
        g_img[self.argmax_x][self.argmax_y] = 0
        b_img[self.argmax_x][self.argmax_y] = 1

        p_img = np.dstack([b_img, g_img, r_img])
        p_img = cv2.resize(p_img, (width, height), interpolation=cv2.INTER_NEAREST)#INTER_AREA
        cv2.imshow('simple_env', p_img)
        cv2.waitKey(approx_wait_time)

    def __repr__(self):
        return "SimpleEnv"


