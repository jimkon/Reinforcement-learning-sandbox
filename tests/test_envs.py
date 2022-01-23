import unittest

from src.rl.core import envs


class TestEnvs(unittest.TestCase):

    def test_gym_envs_list(self):
        gym_envs = envs.gym_envs_list()
        self.assertIsNotNone(gym_envs)
        self.assertTrue(len(gym_envs) > 0)

    def test_wrappable_envs(self):
        gym_envs = envs.gym_envs_list()
        wrapped_envs = envs.wrappable_gym_envs()

        self.assertIsNotNone(wrapped_envs)
        self.assertTrue(len(wrapped_envs) > 0)
        self.assertTrue(len(wrapped_envs) <= len(gym_envs))

    def test_wrap_env(self):
        self.assertIsNotNone(envs.wrap_env('MountainCar-v0'))
        self.assertIsNone(envs.wrap_env('random-text'))
        self.assertIsNone(envs.wrap_env(None))

    def test_is_action_space_discrete(self):
        self.assertTrue(envs.wrap_env('MountainCar-v0').is_action_space_discrete())
        self.assertTrue(not envs.wrap_env('MountainCarContinuous-v0').is_action_space_discrete())

    def test_state_dims(self):
        wrappable_envs = envs.wrappable_gym_envs()

        for env_id in wrappable_envs:
            env = envs.EnvWrapper(env_id)
            self.assertTrue(env.state_dims() > 0)

    def test_state_limits(self):
        wrappable_envs = envs.wrappable_gym_envs()

        for env_id in wrappable_envs:
            env = envs.EnvWrapper(env_id)
            state_lims = env.state_limits()
            state_low, state_high = state_lims[0], state_lims[1]
            diff = state_high-state_low
            self.assertTrue(all(diff >= 0))

    def test_action_dims(self):
        wrappable_envs = envs.wrappable_gym_envs()

        for env_id in wrappable_envs:
            env = envs.EnvWrapper(env_id)
            self.assertTrue(env.action_dims() > 0)
            if env.is_action_space_discrete():
                self.assertTrue(env.action_dims() == 1)

    def test_action_limits(self):
        wrappable_envs = envs.wrappable_gym_envs()

        for env_id in wrappable_envs:
            env = envs.EnvWrapper(env_id)
            action_lims = env.action_limits()
            action_low, action_high = action_lims[0], action_lims[1]
            diff = action_high-action_low
            self.assertTrue(all(diff >= 0))


if __name__ == '__main__':
    unittest.main()
