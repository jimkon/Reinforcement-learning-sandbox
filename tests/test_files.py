import unittest

import pandas as pd
pd.set_option('display.max_columns', None)
import numpy as np

from sqlalchemy.exc import OperationalError

from rl.core import files


class TestFiles(unittest.TestCase):
    def test_db(self):
        self.assertIsNotNone(files.get_engine())

        files.execute_query("drop table if exists test_table")
        self.assertRaises(OperationalError, files.execute_query, "select * from test_table")

        files.execute_query("create table test_table(test_col text)")
        self.assertEqual(len(files.execute_query_and_return("select * from test_table")), 0)

        files.execute_query("drop table test_table")

    def test_experiments_table(self):
        files.execute_query("delete from experiments where experiment_id='test_experiment_id'")
        self.assertFalse(files.check_if_exp_id_already_exists('test_experiment_id'))

        files.execute_query("insert into experiments(experiment_id) values ('test_experiment_id')")
        self.assertTrue(files.check_if_exp_id_already_exists('test_experiment_id'))

        files.execute_query("delete from experiments where experiment_id='test_experiment_id'")
        files.add_experiment_info('test_experiment_id')
        self.assertTrue(files.check_if_exp_id_already_exists('test_experiment_id'))

        files.execute_query("delete from experiments where experiment_id='test_experiment_id'")

    def test_upload_and_download_dfs_on_db(self):
        tablename = 'test_table'
        N = 10

        df = pd.DataFrame({
            'episode': np.arange(N),
            'col_0': np.random.random(size=N),
            'col_1': np.random.random(size=N),
            'col_2': np.random.random(size=N),
            'col_3': np.random.random(size=N),
        })
        df['experiment_id'] = 'test_experiment_id'

        files.execute_query(f"drop table if exists {tablename}")
        files.upload_df_in_db(df, to_table=tablename)
        res_df = files.download_df_from_db('test_experiment_id', from_table=tablename)

        self.assertTrue((df == res_df).all().all())#self.assertTrue(df.equals(res_df))
        files.execute_query(f"drop table {tablename}")

    def test_data_to_df(self):
        df = pd.DataFrame({
            'episode': [0, 0, 0, 1, 1, 1, 1, 1, 2, 2],
            'step': [0, 1, 2, 0, 1, 2, 3, 4, 0, 1],
            'state_0': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            'state_1': [10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            'action_0': [100, 101, 102, 103, 104, 105, 106, 107, 108, 109],
            'reward': [110, 111, 112, 113, 114, 115, 116, 117, 118, 119],
            'done': [0, 1, -1, 0, 0, 0, 1, -1, 1, -1],
        })

        episodes = df['episode'].tolist()
        steps_list = df['step'].tolist()
        states = list(zip(df['state_0'].tolist(), df['state_1'].tolist()))
        actions = [[a] for a in df['action_0'].tolist()]
        rewards = df['reward'].tolist()
        dones = df['done'].tolist()

        res_df = files.data_to_df(episodes, steps_list, states, actions, rewards, dones, compressed=True)
        self.assertTrue((df == res_df).all().all())#self.assertTrue(df.equals(res_df))

        df2 = pd.DataFrame({
            'episode': [0, 0, 1, 1, 1, 1, 2],
            'step': [0, 1, 0, 1, 2, 3, 0],
            'state_0': [0, 1, 3, 4, 5, 6, 8],
            'state_1': [10, 11, 13, 14, 15, 16, 18],
            'action_0': [100, 101, 103, 104, 105, 106, 108],
            'reward': [110, 111, 113, 114, 115, 116, 118],
            'next_state_0': [1, 2, 4, 5, 6, 7, 9],
            'next_state_1': [11, 12, 14, 15, 16, 17, 19],
            'done': [0, 1, 0, 0, 0, 1, 1],
        })
        res_df = files.data_to_df(episodes, steps_list, states, actions, rewards, dones, compressed=False)
        self.assertTrue((df2.reset_index(drop=True) == res_df.reset_index(drop=True)).all().all())#self.assertTrue(df.equals(res_df))


if __name__ == '__main__':
    unittest.main()
