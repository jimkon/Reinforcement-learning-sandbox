from os.path import join, exists

import pandas as pd

from rl.src.core.configs.storage_configs import DB_EXPERIMENT_TABLE_NAME_COL_EXPID,\
                                        DB_EXPERIMENT_TABLE_NAME_COL_EPISODES,\
                                        DB_EXPERIMENT_TABLE_NAME_COL_STEPS,\
                                        DB_EXPERIMENT_TABLE_NAME_COL_STATES,\
                                        DB_EXPERIMENT_TABLE_NAME_COL_NEXTSTATES,\
                                        DB_EXPERIMENT_TABLE_NAME_COL_ACTIONS,\
                                        DB_EXPERIMENT_TABLE_NAME_COL_REWARDS,\
                                        DB_EXPERIMENT_TABLE_NAME_COL_DONE

from rl.src.core.configs.general_configs import EXPERIMENT_STORE_DATAFRAMES_DIRECTORY_ABSPATH,\
                                                STORE_COMPRESSED_DATA

from rl.src.core.utilities.timestamp import timestamp_str, timestamp_long_str
from rl.src.core.utilities.file_utils import create_path
from rl.src.core.storage.db import upload_df_in_db, check_if_exp_id_already_exists


def _generate_df_filename(path_to_file, suggested_name):
    name = suggested_name
    if not name:
        name = f"default_df_name_{timestamp_str()}.csv"

    if ".csv" not in name:
        name += ".csv"

    filepath = join(path_to_file, name)

    if exists(filepath):
        name = suggested_name
        if not name:
            name = f"default_df_name_{timestamp_long_str()}.csv"

        if ".csv" not in name:
            name += ".csv"

        filepath = join(path_to_file, name)

    if exists(filepath):
        raise FileExistsError(f"File {filepath} already exists")

    return filepath


def _generate_valid_experiment_id(suggested_experiment_id):
    experiment_id = suggested_experiment_id
    if not experiment_id:
        experiment_id = f"default_experiment_id_{timestamp_str()}"

    if not check_if_exp_id_already_exists(experiment_id):
        experiment_id = f"default_experiment_id_{timestamp_long_str()}"

    if not check_if_exp_id_already_exists(experiment_id):
        raise ValueError(f"Experiment id {experiment_id} already exists")

    return experiment_id


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
    path_to_file = join(EXPERIMENT_STORE_DATAFRAMES_DIRECTORY_ABSPATH)
    create_path(path_to_file)

    filepath = _generate_df_filename(path_to_file, name)

    df.to_csv(filepath, index=False)

    return filepath


def store_results_as_dataframe(results_dict, name=None):
    df = data_to_df(results_dict)
    if STORE_COMPRESSED_DATA:
        df = compress_data_df(df)
    store_dataframe(df, name=name)


def store_results_in_database(results_dict,
                              to_table,
                              experiment_id=None,
                              agent_id=None,
                              env_id=None,
                              start_time=None,
                              end_time=None,
                              comment=None):
    df = data_to_df(results_dict)
    df_compressed = compress_data_df(df)

    experiment_id = _generate_valid_experiment_id(experiment_id)

    df_compressed[DB_EXPERIMENT_TABLE_NAME_COL_EXPID] = experiment_id

    upload_df_in_db(df_compressed, to_table)

    #TODO add_experiment_info

