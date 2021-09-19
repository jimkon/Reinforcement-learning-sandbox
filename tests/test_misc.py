import os
import unittest

import numpy as np

from experiments.misc import *


class TestClip(unittest.TestCase):
    def test_clip(self):
        self.assertEqual(clip(0, 1, 4), 1)
        self.assertEqual(clip(1, 1, 4), 1)
        self.assertEqual(clip(.999, 1, 4), 1)
        self.assertEqual(clip(2, 1, 4), 2)
        self.assertEqual(clip(3, 1, 4), 3)
        self.assertEqual(clip(4, 1, 4), 4)
        self.assertEqual(clip(4.001, 1, 4), 4)
        self.assertEqual(clip(5, 1, 4), 4)

        self.assertRaises(AttributeError, clip, 3, 3, 1)


class TestMap1D(unittest.TestCase):
    def test_map_init(self):
        self.assertIsNotNone(Map1D(0, 1, 0, 10))
        self.assertRaises(AttributeError, Map1D, 1, 0, 0, 10)
        self.assertRaises(AttributeError, Map1D, 0, 0, 0, 10)
        self.assertRaises(AttributeError, Map1D, 0, 1, 10, 10)

    def test_map_scale_unclipped(self):
        map_unclipped = Map1D(4, 5, 0, 10, clip=False)
        self.assertEqual(map_unclipped(2), -20)
        self.assertEqual(map_unclipped(3), -10)
        self.assertEqual(map_unclipped(3.5), -5)
        self.assertEqual(map_unclipped(4), 0)
        self.assertEqual(map_unclipped(4.5), 5)
        self.assertEqual(map_unclipped(5), 10)
        self.assertEqual(map_unclipped(6), 20)

    def test_map_scale_clipped(self):
        map_clipped = Map1D(4, 5, 0, 10, clip=True)
        self.assertEqual(map_clipped(2), 0)
        self.assertEqual(map_clipped(3), 0)
        self.assertEqual(map_clipped(3.5), 0)
        self.assertEqual(map_clipped(4), 0)
        self.assertEqual(map_clipped(4.5), 5)
        self.assertEqual(map_clipped(5), 10)
        self.assertEqual(map_clipped(6), 10)

    def test_map_inv_scale_unclipped(self):
        map_unclipped = Map1D(4, 5, 10, 0, clip=False)
        self.assertEqual(map_unclipped(2), 30)
        self.assertEqual(map_unclipped(3), 20)
        self.assertEqual(map_unclipped(3.5), 15)
        self.assertEqual(map_unclipped(4), 10)
        self.assertEqual(map_unclipped(4.5), 5)
        self.assertEqual(map_unclipped(5), 0)
        self.assertEqual(map_unclipped(6), -10)

    def test_map_inv_scale_clipped(self):
        map_clipped = Map1D(4, 5, 10, 0, clip=True)
        self.assertEqual(map_clipped(2), 10)
        self.assertEqual(map_clipped(3), 10)
        self.assertEqual(map_clipped(3.5), 10)
        self.assertEqual(map_clipped(4), 10)
        self.assertEqual(map_clipped(4.5), 5)
        self.assertEqual(map_clipped(5), 0)
        self.assertEqual(map_clipped(6), 0)


if __name__ == '__main__':
    unittest.main()
