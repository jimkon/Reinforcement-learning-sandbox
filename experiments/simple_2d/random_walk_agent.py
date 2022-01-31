import random

from rl.src.core.agents import Agent

DIR = [
        [-1, 1],
        [-1, 0],
        [-1, -1],
        [0, -1],
        [0, 0],
        [0, 1],
        [1, -1],
        [1, 0],
        [1, 1],
    ]


class RandomWalkAgent(Agent):

    def __init__(self):
        self.step_count = -1
        self.direction_duration = 0
        self.direction = 0

    def act(self, state):
        self.step_count += 1

        if self.step_count == self.direction_duration:
            self.step_count = 0
            self.direction_duration = random.randint(3, 10)
            self.direction = random.randint(0, len(DIR)-1)

        return DIR[self.direction]

    def name(self):
        return 'Random Walk Agent'



