import numpy as np
import sqlite3 as sql


def db_path():
    """Return the path where databases are stored"""
    import os
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '../../dbs/'))


def create_table_query(name, *fields):
    """Returns a query string where a table with certain values is creates.

    Keyword arguments:
    name -- name of the table
    values -- list of "field name field value"
    """
    return "CREATE TABLE {} ({})".format(name, ", ".join(fields))

print(create_table_query('table', 'value1 real'))
# class rl_db(Object):
#
#     def __init__(self, name):
#         self.conn = sql.connect("{}/{}.db".format(db_path(), name))
#         self.cursor = self.conn.cursor()
#
#     def scheme(self):
#         pass
