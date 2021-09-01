import numpy as np


class Agent:

    def act(self, state):
        raise NotImplementedError

    def observe(self, state, action, reward, next_state, done):
        pass

    def name(self):
        return 'default_agent'


class RandomAgent(Agent):
    def __init__(self, n_actions):
        # self.states_dims = states_dims
        self.n_actions = n_actions

        # self.q_table = np.random.random((self.n_actions, *self.states_dims))

    def act(self, state):
        return np.random.randint(0, self.n_actions)



if __name__=="__main__":
    import gym
    from rl.core.engine import run_episodes
    from rl.core.db import DB
    env = gym.make('MountainCar-v0')
    agent = RandomAgent(3)

    run_episodes(env, agent, 2, render=False, verbosity='episode_step')


    db = DB('rl.db')
    res = db.execute_and_return('select distinct(exp_id) from <TimeLimit<MountainCarEnv<MountainCar-v0>>>')
    print(res)
