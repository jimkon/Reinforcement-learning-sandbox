import unittest

import pandas as pd
pd.set_option('display.max_columns', None)

from rl.core.storage.storage import *


class TestStorage(unittest.TestCase):
    def test_df_filename(self):
        pass

    def test_store_dataframe(self):
        df = pd.get_dummies(pd.Series(list('abc')), dtype=float)
        store_dataframe(df)

