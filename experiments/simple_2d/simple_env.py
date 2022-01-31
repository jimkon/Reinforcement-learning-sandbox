import time

import numpy as np
import cv2
import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise

from rl.src.core.envs import AbstractEnv

def perlin_map(width=100, height=100, octaves=3, seed=1):
    noise = PerlinNoise(octaves=octaves, seed=seed)
    xpix, ypix = width, height
    pic = np.array([[noise([i / xpix, j / ypix]) for j in range(xpix)] for i in range(ypix)])
    pic -= pic.min()
    pic /= pic.max()

    return np.array(pic)


class SimpleEnv(AbstractEnv):

    def __init__(self):
        self.width, self.height = 100, 100
        self.map = perlin_map(width=self.width, height=self.height)
        self.min_action, self.max_action = -1, 1
        self.steps_per_episode = 200

        self.x, self.y = -1, -1
        self.step_count = -1

        self.render_last_time = time.time()-10
        plt.ion()

    def reset(self):
        self.x, self.y = 50, 50
        self.step_count = -1
        state = [self.x, self.y]
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

        reward = self.map[self.x][self.y]

        self.step_count += 1

        done = self.step_count == self.steps_per_episode
        return next_state, reward, done, None

    # def render(self):
    #     now = time.time()
    #     fps = 1/(now-self.render_last_time)
    #
    #     img = cv2.resize(self.map, [300, 300])
    #     # cv2.putText(img, str(round(fps)), (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (1, 0 ,0))
    #     cv2.imshow(str(self), img)
    #     # plt.colorbar()
    #     cv2.waitKey(33)

    def render(self):
        plt.imshow(self.map)
        plt.plot(self.x, self.y, 'ro')
        plt.draw()
        plt.pause(0.001)
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


