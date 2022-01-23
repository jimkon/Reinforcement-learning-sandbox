import pandas as pd


from src.rl.core.configs.experiment import STORE_DATABASE_OBJECT_ABSPATH

from src.rl.core.envs import AbstractEnv

row_num_obj = [-1]
df = pd.DataFrame({
            'episode': [0, 0, 0, 1, 1, 1, 1, 1, 2, 2],
            'step': [0, 1, 2, 0, 1, 2, 3, 4, 0, 1],
            'state_0': [1, 2, 3, 4, 5, 6, 7, 8, 9, 0],
            'state_1': [11, 12, 13, 14, 15, 16, 17, 18, 19, 10],
            'action_0': [100, 101, 102, 103, 104, 105, 106, 107, 108, 109],
            'reward': [110, 111, 112, 113, 114, 115, 116, 117, 118, 119],
            'done': [0, 1, -1, 0, 0, 0, 1, -1, 1, -1],
        })


class TestEnv(AbstractEnv):
    def __init__(self):
        self.df = df
        # self.row_num = 0

    def reset(self):
        # print('reset', row_num_obj[0])
        res = [self.df['state_0'].tolist()[row_num_obj[0]], self.df['state_1'].tolist()[row_num_obj[0]]]
        row_num_obj[0] += 1
        return res

    def step(self, action):
        # print('step', row_num_obj[0])
        res = [self.df['state_0'].tolist()[row_num_obj[0]], self.df['state_1'].tolist()[row_num_obj[0]]]
        done = self.df['done'].tolist()[row_num_obj[0]]
        reward = 110 + row_num_obj[0]
        row_num_obj[0] += 1
        return res, reward, done, None

    def __repr__(self):
        return 'test_env'


class TestAgent:
    def __init__(self):
        self.df = df
        # self.row_num = 0

    def act(self, state):
        res = self.df['action_0'].tolist()[row_num_obj[0]]
        # self.row_num += 1
        return res

    def set_env(self, env):
        pass

    def observe(self, *args):
        pass

    def name(self):
        return 'test_agent'


if __name__=="__main__":
    print(STORE_DATABASE_OBJECT_ABSPATH)
    exit()
    from src.rl.core.engine import run_episodes

    agent = TestAgent()
    env = TestEnv()

    run_episodes(env,
                agent,
                3,
                experiment_name='test',
                store_results='dataframe')