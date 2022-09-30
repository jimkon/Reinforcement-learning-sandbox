from os.path import join, exists

import pandas as pd

from rl.core.configs.storage_configs import DB_EXPERIMENT_TABLE_NAME_COL_EXPID, \
    DB_EXPERIMENT_TABLE_NAME_COL_EPISODES, \
    DB_EXPERIMENT_TABLE_NAME_COL_STEPS, \
    DB_EXPERIMENT_TABLE_NAME_COL_STATES, \
    DB_EXPERIMENT_TABLE_NAME_COL_ACTIONS, \
    DB_EXPERIMENT_TABLE_NAME_COL_REWARDS, \
    DB_EXPERIMENT_TABLE_NAME_COL_DONE, DB_EXPERIMENT_TABLE_NAME_COL_NEXTSTATES

from rl.core.configs.path_confgis import EXPERIMENT_DATAFRAMES_DIRECTORY_ABSPATH

from rl.core.utilities.timestamp import timestamp_str, timestamp_long_str
from rl.core.storage.db import upload_df_in_db,\
                                    exp_id_already_exists,\
                                    add_experiment_info


def data_to_df(results_dict):
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
        to_dict[f"{DB_EXPERIMENT_TABLE_NAME_COL_ACTIONS}_{i}"] = [a if a != 'null' else None for a in action_i]

    to_dict[DB_EXPERIMENT_TABLE_NAME_COL_REWARDS] = rewards

    to_dict[DB_EXPERIMENT_TABLE_NAME_COL_DONE] = list(map(int, dones))

    df = pd.DataFrame(to_dict)

    return df


def compress_data_df(df):#TODO
    dones = df[DB_EXPERIMENT_TABLE_NAME_COL_DONE]
    del df[DB_EXPERIMENT_TABLE_NAME_COL_DONE]
    state_cols = [col for col in df.columns if DB_EXPERIMENT_TABLE_NAME_COL_STATES in col]
    for i, c in enumerate(state_cols):
        df[f"{DB_EXPERIMENT_TABLE_NAME_COL_NEXTSTATES}_{i}"] = df[f"{DB_EXPERIMENT_TABLE_NAME_COL_STATES}_{i}"].shift(periods=-1)

    df[DB_EXPERIMENT_TABLE_NAME_COL_DONE] = dones

    df = df[df[DB_EXPERIMENT_TABLE_NAME_COL_DONE] >= 0]

    return df


# def store_results_in_database(results_dict,
#                               to_table,
#                               experiment_id=None,
#                               agent_id=None,
#                               env_id=None,
#                               start_time=None,
#                               duration_secs=None,
#                               comment=None):
#     df = data_to_df(results_dict)
#     # df_compressed = compress_data_df(df)#TODO
#
#     experiment_id = _generate_valid_experiment_id(experiment_id)
#
#     df[DB_EXPERIMENT_TABLE_NAME_COL_EXPID] = experiment_id
#
#     upload_df_in_db(df, to_table)
#
#     add_experiment_info(
#         experiment_id,
#         agent_id=agent_id,
#         env_id=env_id,
#         total_reward=df[DB_EXPERIMENT_TABLE_NAME_COL_REWARDS].sum(),
#         episodes=df[DB_EXPERIMENT_TABLE_NAME_COL_EPISODES].max()-len(df),
#         total_steps=len(df),
#         start_time=start_time,
#         duration_secs=duration_secs,
#         comment=comment
#     )
#
#     #TODO add_experiment_info

