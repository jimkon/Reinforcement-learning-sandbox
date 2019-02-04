import numpy as np
import sqlite3 as sql

def db_path():
    import os
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '../../dbs/'))

class rl_db(Object):

    def __init__(self, name):
        self.conn = sql.connect("{}/{}.db".format(db_path(), name))
        self.cursor = self.conn.cursor()

    def scheme(self):
        
