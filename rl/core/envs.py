import numpy as np
import gym

from functools import lru_cache


@lru_cache()
def gym_env_list():
    envids = sorted([spec.id for spec in gym.envs.registry.all()])
    return envids


class EnvScraper:
    def __init__(self, gym_env_id):
        self.env_id = gym_env_id
        self.gym_env = gym.make(gym_env_id)
        self.gym_env.reset()
        assert self.gym_env.state is not None
        assert self.gym_env.observation_space is not None
        assert self.gym_env.action_space is not None

        observation_space = self.gym_env.observation_space
        if not isinstance(observation_space, gym.spaces.box.Box) and not isinstance(observation_space, gym.spaces.discrete.Discrete):
            raise Exception('Unknown observation space type for this environment: '+str(type(observation_space)))

        self.state_low = observation_space.low if isinstance(observation_space, gym.spaces.box.Box) else [0]
        self.state_high = observation_space.high if isinstance(observation_space, gym.spaces.box.Box) else [observation_space.n-1]

        action_space = self.gym_env.action_space
        if not isinstance(action_space, gym.spaces.box.Box) and not isinstance(action_space,
                                                                                    gym.spaces.discrete.Discrete):
            raise Exception('Unknown action space type for this environment: ' + str(type(action_space)))

        self.action_low = action_space.low if isinstance(action_space, gym.spaces.box.Box) else [0]
        self.action_high = action_space.high if isinstance(action_space, gym.spaces.box.Box) else [
                action_space.n-1]

    @lru_cache()
    def state_dims(self):
        return len(self.state_low)

    @lru_cache()
    def state_limits(self):
        res = np.array([self.state_low, self.state_high])
        return res

    @lru_cache()
    def action_dims(self):
        return len(self.action_low)

    @lru_cache()
    def action_limits(self):
        res = np.array([self.action_low, self.action_high])
        return res

    @lru_cache()
    def is_action_space_discrete(self):
        return isinstance(self.gym_env.action_space, gym.spaces.discrete.Discrete)

    def __step(self, state, action):
        self.gym_env.state = state
        next_state, reward, done, _ = self.gym_env.step(action)
        return next_state, reward, done

    # walks
    def init_state(self):
        return self.gym_env.reset()

    def transition(self, state, action):
        next_state, reward, done = self.__step(tuple(state), tuple(action))
        return next_state

    def reward(self, state, action):
        next_state, reward, done = self.__step(state, action)
        return reward

    def is_done(self, state, action):
        next_state, reward, done = self.__step(tuple(state), tuple(action))
        return done

    def info(self):
        print_format = "%(env_id)s: state_dims:%(state_dims)s state_limits:%(state_limits)s action_dims:%(action_dims)s action_limits:%(action_limits)s"
        env_id = self.env_id
        state_dims = self.state_dims()
        state_limits = "(%s %s)" % (self.state_low, self.state_high)
        action_dims = self.action_dims()
        action_limits = "(%s %s)" % (self.action_low, self.action_high)
        print(print_format % locals())

    def random_state(self):
        return self.gym_env.observation_space.sample()

    def random_action(self):
        return self.gym_env.action_space.sample()


@lru_cache()
def scrapable_envs():
    res = []
    for env_id in gym_env_list():
        try:
            EnvScraper(env_id)
        except Exception as e:
            pass
            # print(e)
        else:
            res.append(env_id)
    return res
