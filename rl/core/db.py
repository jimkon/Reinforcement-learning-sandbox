import os
from functools import lru_cache

import pandas as pd
import sqlite3 as sql

DB_FILE_EXTENSION = '.db'


def log(msg, type='info'):
    print(msg)

@lru_cache
def db_path():
    """Return the path where databases are stored"""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '../../dbs/'))


def stored_dbs_names():
    all_files = os.listdir(db_path())
    all_dbs = [os.path.join(db_path(), db_name) for db_name in all_files if db_name[-3:] == DB_FILE_EXTENSION]
    return all_dbs


# def init_db(db_name):
#     db_abs_path = os.path.join(db_path(), db_name)
#
#     if db_abs_path in stored_dbs_names():
#         log("Opening existing db file in path"+db_abs_path)
#     else:
#         log("Creating new db file in path"+db_abs_path)
#
#     return DB(db_name)


class DB:
    def __init__(self, db_name, log_file=None):
        if db_name[-3:] != DB_FILE_EXTENSION:
            db_name += DB_FILE_EXTENSION

        self.db_name = db_name
        self.__abs_path = os.path.join(db_path(), db_name)
        self.__conn = sql.connect(self.__abs_path)
        self.__cursor = self.__conn.cursor()
        self.__log_file = log_file

    def execute(self, query):
        return self.__cursor.execute(query)

    def execute_and_return(self, query):
        return pd.read_sql_query(query, self.__conn)

    def close(self):
        self.__cursor.close()
        self.__conn.close()
