import context
import unittest

from rl.core import db_logger as db

class TestQueries(unittest.TestCase):

    def test_create_table_query(self):
        self.assertEqual(db.create_table_query('table', 'v1 real'), 'CREATE TABLE table (v1 real)')
