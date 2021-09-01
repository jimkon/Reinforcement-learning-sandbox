import os
import sys
from functools import lru_cache
from traceback import format_exc


import pandas as pd
import sqlite3 as sql

import rl.core.configs as configs

"""
TODO:
default db object
"""

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
    def __init__(self, db_name, log_file=None, verbose=None):
        if db_name[-3:] != DB_FILE_EXTENSION:
            db_name += DB_FILE_EXTENSION

        self.db_name = db_name
        self.__abs_path = os.path.join(db_path(), db_name)
        self.__conn = sql.connect(self.__abs_path)
        self.__cursor = self.__conn.cursor()
        self.__log_file = log_file

        self.verbose = verbose if verbose else configs.DB_VERBOSITY

    def execute(self, query, verbose=0, error_log_file=None):
        verbose = max(self.verbose, verbose)
        if verbose > 0:
            print(query)

        try:
            self.__cursor.execute(query)
            return True
        except Exception as e:
            print("EXCEPTION IN DATABASE:")
            print(format_exc(), sys.stderr if not error_log_file else error_log_file)
            print("EXCEPTION PRODUCED BY QUERY:")
            print(query, sys.stderr if not error_log_file else error_log_file)
            return None

    def execute_and_return(self, query, verbose=0, error_log_file=None):
        verbose = max(self.verbose, verbose)
        if verbose > 0:
            print(query)
        try:
            return pd.read_sql_query(query, self.__conn)
        except Exception as e:
            print("EXCEPTION IN DATABASE:")
            print(format_exc(), sys.stderr if not error_log_file else error_log_file)
            print("EXCEPTION PRODUCED BY QUERY:")
            print(query, sys.stderr if not error_log_file else error_log_file)
            return None


    def close(self):
        self.__cursor.close()
        self.__conn.close()


def default_db():
    return DB(db_path()+"/"+configs.DB_DEFAULT_DB_NAME+DB_FILE_EXTENSION)
