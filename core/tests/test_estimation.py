from unittest import TestCase

import numpy as np
from numpy.testing import assert_array_equal
from core.estimation import hamming_distance, const


class TestHammingDistance(TestCase):

    def test_empty(self):
        pop = np.zeros((10, 5), dtype=np.int8)
        health = hamming_distance(pop)

        self.assertEqual(health.shape, (10,))
        self.assertEqual(health.dtype, np.int32)
        assert_array_equal(
            health,
            np.zeros(10, dtype=np.int8)
        )

    def test_health(self):
        pop = np.array(
            [
                [0, 1, 0, 0, 1],
                [0, 1, 1, 0, 1],
                [1, 1, 1, 1, 1],
            ],
            dtype=np.int8
        )
        health = hamming_distance(pop)
        assert_array_equal(
            health,
            np.array([2, 3, 5], dtype=np.int32)
        )


class TestConst(TestCase):

    def test_empty(self):
        length = 5
        pop = np.zeros((10, length), dtype=np.int8)

        health = const(pop)
        self.assertEqual(health.shape, (10,))
        self.assertEqual(health.dtype, np.int32)
        self.assertTrue(np.any(health == length))
