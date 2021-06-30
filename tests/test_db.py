import os
import unittest

import numpy as np

from rl.core import db


class TestFunctions(unittest.TestCase):
    def test_stored_dbs_names(self):
        test_files = []
        def create_file(filename):
            path = os.path.join(db.db_path(), filename)
            with open(path, 'w') as f:
                f.write("test")
                test_files.append(path)

        create_file('test1.db')
        create_file('test2.db')
        create_file('test3.aa')
        create_file('test4.bb')
        create_file('test5.db')

        dbs = db.stored_dbs_names()

        self.assertTrue(os.path.join(db.db_path(), 'test1.db') in dbs)
        self.assertTrue(os.path.join(db.db_path(), 'test2.db') in dbs)
        self.assertTrue(os.path.join(db.db_path(), 'test3.aa') not in dbs)
        self.assertTrue(os.path.join(db.db_path(), 'test4.bb') not in dbs)
        self.assertTrue(os.path.join(db.db_path(), 'test5.db') in dbs)

        for file in test_files:
            os.remove(file)


class TestDB(unittest.TestCase):
    def setUp(self):
        os.remove(os.path.join(db.db_path(), 'test_db.db'))
        self.db_obj = db.DB('test_db.db')
        self.db_obj.execute("create table table1 (id integer);")
        self.db_obj.execute("insert into table1(id) values(1),(2),(3);")

    def tearDown(self):
        self.db_obj.close()
        os.remove(os.path.join(db.db_path(), self.db_obj.db_name))

    def test_execute_and_return(self):
        res = self.db_obj.execute_and_return('select * from table1').to_numpy()
        self.assertTrue(all(np.equal(res, [[1], [2], [3]])))



