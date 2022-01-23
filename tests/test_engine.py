import unittest

import pandas as pd

from src.rl.core import engine
from src.rl.core import download_df_from_db, execute_query, execute_query_and_return


class TestEngineMisc(unittest.TestCase):
    def test_env_name_to_table(self):
        self.assertEqual(engine.env_name_to_table('<a<b<table-name>>>'), 'table_name')
        self.assertEqual(engine.env_name_to_table('table-name'), 'table_name')


class TestEngine(unittest.TestCase):

    def setUp(self):
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

        class TestEnv:
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
                reward = 110+row_num_obj[0]
                row_num_obj[0] += 1
                return res, reward, done, None

            def __repr__(self):
                return 'test_env'

        self.agent = TestAgent()
        self.env = TestEnv()

    def tearDown(self):
        pass

    def test_run_episodes_dataframe(self):
        expected_res_df = pd.DataFrame({
            'episode': [0, 0, 1, 1, 1, 1, 2],
            'step': [0, 1, 0, 1, 2, 3, 0],
            'state_0': [0, 1, 3, 4, 5, 6, 8],
            'state_1': [10, 11, 13, 14, 15, 16, 18],
            'action_0': [100, 101, 103, 104, 105, 106, 108],
            'reward': [110, 111, 113, 114, 115, 116, 118],
            'next_state_0': [1, 2, 4, 5, 6, 7, 9],
            'next_state_1': [11, 12, 14, 15, 16, 17, 19],
            'done': [0, 1, 0, 0, 0, 1, 1],
            'experiment_id': ['test']*7
        })
        engine.run_episodes(self.env,
                            self.agent,
                            3,
                            experiment_name='test',
                            store_results='database')

        res_df = download_df_from_db('test', 'test_env')
        # res_df = pd.read_csv("../files/results/dataframes/test.csv")
        self.assertTrue((expected_res_df.reset_index(drop=True) == res_df.reset_index(drop=True)).all().all())#self.assertTrue(df.equals(res_df))

        print(execute_query_and_return("select * from experiments where experiment_id='test'"))
        # self.assertTrue()
        execute_query("delete from experiments where experiment_id='test'")
        execute_query("drop table test_env")


if __name__ == '__main__':
    unittest.main()


