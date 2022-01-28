from os.path import join

import pandas as pd

from rl.src.core.configs.storage_configs import DB_EXPERIMENT_TABLE_NAME_COL_EPISODES,\
                                        DB_EXPERIMENT_TABLE_NAME_COL_STEPS,\
                                        DB_EXPERIMENT_TABLE_NAME_COL_STATES,\
                                        DB_EXPERIMENT_TABLE_NAME_COL_NEXTSTATES,\
                                        DB_EXPERIMENT_TABLE_NAME_COL_ACTIONS,\
                                        DB_EXPERIMENT_TABLE_NAME_COL_REWARDS,\
                                        DB_EXPERIMENT_TABLE_NAME_COL_DONE

from rl.src.core.configs.general_configs import EXPERIMENT_ROOT_ABSPATH,\
                                                DEFAULT_STORE_DATAFRAMES_DIRECTORY_PATH,\
                                                STORE_COMPRESSED_DATA

from rl.src.core.utilities.timestamp import timestamp_str
from rl.src.core.utilities.file_utils import create_path


def data_to_df(results_dict):
    print(results_dict)
    episodes = results_dict[DB_EXPERIMENT_TABLE_NAME_COL_EPISODES]
    steps_list = results_dict[DB_EXPERIMENT_TABLE_NAME_COL_STEPS]
    states = results_dict[DB_EXPERIMENT_TABLE_NAME_COL_STATES]
    actions = results_dict[DB_EXPERIMENT_TABLE_NAME_COL_ACTIONS]
    rewards = results_dict[DB_EXPERIMENT_TABLE_NAME_COL_REWARDS]
    dones = results_dict[DB_EXPERIMENT_TABLE_NAME_COL_DONE]

    to_dict = {
        DB_EXPERIMENT_TABLE_NAME_COL_EPISODES: episodes,
        DB_EXPERIMENT_TABLE_NAME_COL_STEPS: steps_list
    }

    states = list(map(list, zip(*states)))
    for i, state_i in enumerate(states):
        to_dict[f"{DB_EXPERIMENT_TABLE_NAME_COL_STATES}_{i}"] = state_i

    actions = list(map(list, zip(*actions)))
    for i, action_i in enumerate(actions):
        to_dict[f"{DB_EXPERIMENT_TABLE_NAME_COL_ACTIONS}_{i}"] = action_i

    to_dict[DB_EXPERIMENT_TABLE_NAME_COL_REWARDS] = rewards

    to_dict[DB_EXPERIMENT_TABLE_NAME_COL_DONE] = list(map(int, dones))

    df = pd.DataFrame(to_dict)

    return df


def compress_data_df(df):
    dones = df[DB_EXPERIMENT_TABLE_NAME_COL_DONE]
    del df[DB_EXPERIMENT_TABLE_NAME_COL_DONE]
    for i in range(len(df[DB_EXPERIMENT_TABLE_NAME_COL_STATES])):
        df[f"{DB_EXPERIMENT_TABLE_NAME_COL_NEXTSTATES}_{i}"] = df[f"{DB_EXPERIMENT_TABLE_NAME_COL_STATES}_{i}"].shift(periods=-1)

    df[DB_EXPERIMENT_TABLE_NAME_COL_DONE] = dones

    df = df[df[DB_EXPERIMENT_TABLE_NAME_COL_DONE] >= 0]

    return df


def store_dataframe(df, name=None):
    if not name:
        name = f"default_df_name_{timestamp_str()}.csv"
    if not ".csv" in name:
        name += ".csv"
    path = join(EXPERIMENT_ROOT_ABSPATH, DEFAULT_STORE_DATAFRAMES_DIRECTORY_PATH, name)

    create_path(path)

    df.to_csv(path, index=False)


def store_results_as_dataframe(results_dict, name=None):
    df = data_to_df(results_dict)
    if STORE_COMPRESSED_DATA:
        df = compress_data_df(df)
    store_dataframe(df, name=name)
