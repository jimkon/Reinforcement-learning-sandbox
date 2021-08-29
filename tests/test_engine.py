import os
import unittest

import numpy as np

from rl.core import engine, db


class Agent:
    def act(self, state):
        return [state[0], state[1]]

    def observe(self, *args):
        pass

    def name(self):
        return 'test_agent'


class Env:
    def __init__(self):
        self.cnt = 0.

    def reset(self):
        self.cnt = 0.
        return [self.cnt+0.1, self.cnt+0.2, self.cnt+0.3]

    def step(self, action):
        self.cnt += 1
        return [self.cnt+0.1, self.cnt+0.2, self.cnt+0.3], self.cnt, int(np.random.random(1)[0]>0.5), None

    def render(self):
        pass

    def __repr__(self):
        return 'test_env'


# class DB:
#     def execute(self, query):
#         print('DB:\n', query)


class TestEngine(unittest.TestCase):

    def setUp(self):
        self.db_path = os.path.join(db.db_path(), 'test_db.db')
        self.db_obj = db.DB('test_db.db', verbose=1)

        self.agent = Agent()
        self.env = Env()

    def tearDown(self):
        self.db_obj.close()
        os.remove(os.path.join(db.db_path(), self.db_obj.db_name))

    def test_store_results_to_database(self):
        tablename = 'to_table_arg'
        agent_id = 'agent_id_arg'
        experiment_id = 'experiment_id_arg'
        episodes = [0, 1, 1, 1]
        steps_list = [0, 0, 1, 2]
        states = [[0, 0], [1, 11], [2, 22], [3, 33]]
        actions = [[0], [10], [20], [30]]
        rewards = [0, 100, 200, 300]
        dones = [1, 0, 0, 1]
        data = (episodes, steps_list, states, actions, rewards, dones)

        engine.store_results_to_database(self.db_obj,
                                         data,
                                         to_table=tablename,
                                         agent_id=agent_id,
                                         experiment_id=experiment_id)

        res = self.db_obj.execute_and_return("select * from to_table_arg order by episode, step")

        for i, row in res.iterrows():
            self.assertEqual(res.iloc[i]['exp_id'], experiment_id)
            self.assertEqual(res.iloc[i]['agent_id'], agent_id)
            self.assertEqual(res.iloc[i]['episode'], 0 if i == 0 else 1)
            self.assertEqual(res.iloc[i]['state_0'], i)
            self.assertEqual(res.iloc[i]['state_1'], i*11)
            self.assertEqual(res.iloc[i]['action_0'], i*10)
            self.assertEqual(res.iloc[i]['reward'], i*100)
            self.assertEqual(res.iloc[i]['done'], 1 if i == 0 or i == 3 else 0)

    def test_run_episodes(self):
        engine.run_episodes(self.env,
                            self.agent,
                            2,
                            log_database=self.db_obj,
                            log_frequency=-1,
                            verbosity=None)

        res = self.db_obj.execute_and_return(f"select * from {str(self.env)} order by episode, step")

        ep_cnt = 0
        for i, row in res.iterrows():
            done = res.iloc[i]['done']
            step = res.iloc[i]['step']

            self.assertEqual(res.iloc[i]['agent_id'], self.agent.name())
            self.assertEqual(res.iloc[i]['episode'], ep_cnt)

            self.assertEqual(res.iloc[i]['state_0'], step+0.1)
            self.assertEqual(res.iloc[i]['state_1'], step+0.2)
            self.assertEqual(res.iloc[i]['state_2'], step+0.3)
            self.assertTrue(np.isnan(res.iloc[i]['action_0']) if done==-1 else res.iloc[i]['action_0'] == step + 0.1)
            self.assertTrue(np.isnan(res.iloc[i]['action_1']) if done==-1 else res.iloc[i]['action_1'] == step + 0.2)
            self.assertEqual(res.iloc[i]['reward'], step+1 if done>=0 else 0)

            ep_cnt += 1 if done==-1 else 0
