import os
import unittest

import gym
import numpy as np

from rl.core import envs


class TestEnvs(unittest.TestCase):

    def test_gym_envs_list(self):
        gym_envs = envs.gym_envs_list()
        self.assertIsNotNone(gym_envs)
        self.assertTrue(len(gym_envs) > 0)

    def test_wrappable_envs(self):
        gym_envs = envs.gym_envs_list()
        wrapped_envs = envs.wrappable_envs()

        self.assertIsNotNone(wrapped_envs)
        self.assertTrue(len(wrapped_envs) > 0)
        self.assertTrue(len(wrapped_envs) <= len(gym_envs))

    def test_wrap_env(self):
        self.assertIsNotNone(envs.wrap_env('MountainCar-v0'))
        self.assertIsNone(envs.wrap_env('random-text'))
        self.assertIsNone(envs.wrap_env(None))

    def test_is_action_space_discrete(self):
        self.assertTrue(envs.wrap_env('MountainCar-v0'))
        self.assertTrue(not envs.wrap_env('MountainCarContinuous-v0'))

    def test_state_dims(self):
        wrappable_envs = envs.wrappable_envs()

        for env_id in wrappable_envs:
            env = envs.EnvWrapper(env_id)
            self.assertTrue(env.state_dims() > 0)

    def test_state_limits(self):
        wrappable_envs = envs.wrappable_envs()

        for env_id in wrappable_envs:
            env = envs.EnvWrapper(env_id)
            state_lims = env.state_limits()
            state_low, state_high = state_lims[0], state_lims[1]
            diff = state_high-state_low
            self.assertTrue(all(diff >= 0))

    def test_action_dims(self):
        wrappable_envs = envs.wrappable_envs()

        for env_id in wrappable_envs:
            env = envs.EnvWrapper(env_id)
            self.assertTrue(env.action_dims() > 0)
            if env.is_action_space_discrete():
                self.assertTrue(env.action_dims() == 1)

    def test_action_limits(self):
        wrappable_envs = envs.wrappable_envs()

        for env_id in wrappable_envs:
            env = envs.EnvWrapper(env_id)
            action_lims = env.action_limits()
            action_low, action_high = action_lims[0], action_lims[1]
            diff = action_high-action_low
            self.assertTrue(all(diff >= 0))

    def test_inner_methods(self):
        wrappable_envs = envs.wrappable_envs()

        for env_id in wrappable_envs:
            gym_env = gym.make(env_id)
            env = envs.EnvWrapper(env_id)

            gym_initial_state = gym_env.reset()
            random_action = env.random_action()
            print(env_id, random_action)
            gym_next_state, gym_reward, gym_done, _ = gym_env.step(random_action)

            next_state = env.transition(gym_initial_state, random_action)
            # self.assertTrue(all(np.isclose(gym_next_state, next_state, atol=0.01)))
            reward = env.reward(gym_initial_state, random_action)
            self.assertTrue(gym_reward, reward)

            done = env.is_done(gym_initial_state, random_action)
            self.assertTrue(gym_done == done)

            while gym_done:
                gym_initial_state = gym_next_state
                gym_next_state, gym_reward, gym_done, _ = gym_env.step(env.random_action())
                done = env.is_done(gym_initial_state, random_action)
                self.assertTrue(gym_done == done)

