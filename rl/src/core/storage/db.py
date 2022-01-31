
import pandas as pd
import sqlalchemy.exc
from sqlalchemy import create_engine

from rl.src.core.configs.general_configs import EXPERIMENT_STORE_DATABASE_OBJECT_ABSPATH
from rl.src.core.utilities.file_utils import create_path


def __get_engine():
    db_path = EXPERIMENT_STORE_DATABASE_OBJECT_ABSPATH
    create_path(EXPERIMENT_STORE_DATABASE_OBJECT_ABSPATH)

    engine = create_engine('sqlite:///'+db_path, echo=False)

    return engine


def execute_query(query):
    engine = __get_engine()

    with engine.connect() as connection:
        connection.execute(query)


def execute_query_and_return(query):
    engine = __get_engine()

    with engine.connect() as connection:
        result = connection.execute(query)
        return list(result)


def exp_id_already_exists(experiment_id):
    try:
        res = execute_query_and_return(query=f'select experiment_id from experiments where experiment_id="{experiment_id}" limit 1')
        print(res)
    except sqlalchemy.exc.OperationalError as e:
        return False# no such table: experiments

    return res is not None and len(res) > 0


def add_experiment_info(experiment_id,
                        agent_id=None,
                        env_id=None,
                        total_reward=None,
                        episodes=None,
                        total_steps=None,
                        start_time=None,
                        duration_secs=None,
                        comment=None):
    engine = __get_engine()

    args = locals()
    del args['engine']
    for k, v in args.items():
        args[k] = [v]

    df = pd.DataFrame.from_dict(args)
    df.to_sql('experiments', con=engine, if_exists='append', index=False)


def upload_df_in_db(df, to_table):
    engine = __get_engine()

    df.to_sql(to_table, con=engine, if_exists='append', index=False)


def download_df_from_db(experiment_id, from_table):
    engine = __get_engine()

    df = pd.read_sql(f'select * from {from_table} where experiment_id=\"{experiment_id}\"',
                     con=engine,
                     coerce_float=True,
                     index_col='episode').reset_index()

    return df
