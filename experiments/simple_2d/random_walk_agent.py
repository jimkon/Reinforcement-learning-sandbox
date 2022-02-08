import random

from rl.src.core.agents import AbstractAgent
from rl.src.core.logging import Logger

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

logger = Logger('random_walk_agent')


class RandomWalkAgent(AbstractAgent):

    def __init__(self):
        self.step_count = -1
        self.direction_duration = 0
        self.direction = 0

    @logger.log_func_call()
    def act(self, state):
        self.step_count += 1

        if self.step_count == self.direction_duration:
            self.step_count = 0
            self.direction_duration = random.randint(3, 10)
            self.direction = random.randint(0, len(DIR)-1)

        return DIR[self.direction]

    @logger.log_func_call()
    def name(self):
        return 'Random Walk Agent'



