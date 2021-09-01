import time
import os

import pandas as pd
from sqlalchemy import create_engine

from rl.core.configs import STORE_COMPRESSED_DATA, DEFAULT_STORE_DATAFRAMES_DIRECTORY_PATH, DEFAULT_STORE_DATABASE_OBJECT_PATH

"""
TODO 
- unittesting
"""


def store_df_in_db(df, to_table, db_path=None):
    if not db_path:
        db_path = DEFAULT_STORE_DATABASE_OBJECT_PATH

    engine = create_engine('sqlite:///'+db_path, echo=False)

    df.to_sql(to_table, con=engine, if_exists='append', index=False)


def data_to_df(episodes, steps_list, states, actions, rewards, dones):
    to_dict = {}

    to_dict['episode'] = episodes

    to_dict['step'] = steps_list

    states = list(map(list, zip(*states)))
    for i, state_i in enumerate(states):
        to_dict[f"state_{i}"] = state_i

    actions = list(map(list, zip(*actions)))
    for i, action_i in enumerate(actions):
        to_dict[f"action_{i}"] = action_i

    to_dict['reward'] = rewards

    to_dict['done'] = list(map(int, dones))

    df = pd.DataFrame(to_dict)

    if not STORE_COMPRESSED_DATA:
        dones = df['done']
        del df['done']
        for i in range(len(states)):
            df[f"next_state_{i}"] = df[f"state_{i}"].shift(periods=-1)

        df['done'] = dones

        df = df[df['done'] >= 0]

    return df


class StoreResultsAbstract:
    def save(self, episodes, steps_list, states, actions, rewards, dones):
        raise NotImplementedError

    def finalize(self):
        pass


class StoreResultsInDataframe(StoreResultsAbstract):
    def __init__(self, dir_path=None, experiment_name=None, env=None, agent=None):
        self.dir_path = dir_path if dir_path else DEFAULT_STORE_DATAFRAMES_DIRECTORY_PATH

        if experiment_name:
            self.experiment_name = experiment_name
        elif env and agent:
            self.experiment_name = f"{str(env)},{agent.name()}"
        else:
            self.experiment_name = "unknown_env,unknown_agent"

        self.experiment_id = f"{time.strftime('%Y-%m-%d,%H-%M-%S')}"

        self.experiment_dir_path = os.path.join(self.dir_path, self.experiment_name)
        if not os.path.exists(self.experiment_dir_path):
            os.mkdir(self.experiment_dir_path)

        self.experiment_temp_dir_path = os.path.join(self.experiment_dir_path,
                                                     'temp_'+self.experiment_name+'_'+self.experiment_id)
        if not os.path.exists(self.experiment_temp_dir_path):
            os.mkdir(self.experiment_temp_dir_path)

        self.df_path = None

    def save(self, episodes, steps_list, states, actions, rewards, dones):
        df = data_to_df(episodes, steps_list, states, actions, rewards, dones)

        df_path = os.path.join(self.experiment_temp_dir_path,
                               self.experiment_name+','+self.experiment_id+','+str(time.time())+'.csv')

        df.to_csv(df_path, index=False)

    def finalize(self):
        dfs = [os.path.join(self.experiment_temp_dir_path, df_name) for df_name in os.listdir(self.experiment_temp_dir_path)]
        if len(dfs) < 1:
            return
        temp_dfs = [pd.read_csv(df_name, index_col=None) for df_name in dfs]
        res_df = pd.concat(temp_dfs)

        self.df_path = os.path.join(self.experiment_dir_path, self.experiment_name+','+self.experiment_id+'.csv')
        res_df.to_csv(self.df_path, index=False)

        for df_name in dfs:
            os.remove(df_name)
        os.rmdir(self.experiment_temp_dir_path)


class StoreResultsInDatabase(StoreResultsAbstract):
    def __init__(self, to_table, db_path=None, env=None, agent=None):
        self.to_table = to_table
        self.db_path = db_path if db_path else DEFAULT_STORE_DATABASE_OBJECT_PATH

        self.env, self.agent = env, agent

        self.store_in_df = StoreResultsInDataframe(experiment_name=to_table+"_"+time.strftime('%Y-%m-%d,%H-%M-%S'))

    def save(self, episodes, steps_list, states, actions, rewards, dones):
        self.store_in_df.save(episodes, steps_list, states, actions, rewards, dones)

    def finalize(self):
        self.store_in_df.finalize()

        print(self.store_in_df.df_path)

        df = pd.read_csv(self.store_in_df.df_path, index_col=None)
        store_df_in_db(df, self.to_table)
        os.remove(self.store_in_df.df_path)
        if len(os.listdir(self.store_in_df.experiment_dir_path)) == 0:
            os.rmdir(self.store_in_df.experiment_dir_path)




