from unittest import TestCase

import numpy as np
from numpy.testing import assert_array_equal
from estimation import hamming_distance, const, on_split_locuses


class TestHammingDistance(TestCase):

    def test_empty(self):
        pop = np.zeros((10, 5), dtype=np.int8)
        health = hamming_distance(pop)

        self.assertEquals(health.shape, (10,))
        self.assertEquals(health.dtype, np.int32)
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
        self.assertEquals(health.shape, (10,))
        self.assertEquals(health.dtype, np.int32)
        self.assertTrue(np.any(health == length))


class TestOnSplitLocuses(TestCase):

    def test_not_all_locuses(self):
        pop = np.zeros((10, 7), dtype=np.int8)

        kwargs = {
            'population': pop,
            'ar_bad':    np.array([1, 1, 0, 1, 0, 0, 1]),
            'ar_good':   np.array([0, 0, 0, 0, 0, 0, 0]),
            'ar_lethal': np.array([0, 0, 0, 0, 0, 0, 0])
        }

        self.assertRaises(AssertionError, on_split_locuses, **kwargs)

    def test_locuses_intersect(self):
        pop = np.zeros((10, 7), dtype=np.int8)

        kwargs = {
            'population': pop,
            'ar_bad':    np.array([1, 1, 0, 1, 0, 0, 1]),
            'ar_good':   np.array([1, 0, 0, 0, 0, 0, 0]),
            'ar_lethal': np.array([1, 0, 1, 0, 1, 1, 0])
        }

        self.assertRaises(AssertionError, on_split_locuses, **kwargs)

    def test_empty(self):
        pop = np.zeros((10, 7), dtype=np.int8)

        ar___bad = np.array([0, 0, 0, 1, 0, 0, 1], dtype=np.int8)
        ar__good = np.array([1, 0, 1, 0, 0, 1, 0], dtype=np.int8)
        ar_fatal = np.array([0, 1, 0, 0, 1, 0, 0], dtype=np.int8)

        health = on_split_locuses(pop, ar__good, ar___bad, ar_fatal)

        self.assertTrue(np.any(health == 7))

    def test_mixed(self):
        pop = np.array(
            [
                [0, 0, 0, 0, 0],  # health: 5
                [0, 1, 0, 1, 0],  # fatal locus. health: 0.1
                [0, 0, 0, 1, 0],  # bad locus. health: 5 - 10*1 = -5
                [1, 0, 1, 0, 0],  # all good. health: 5
                [1, 0, 1, 1, 0],  # good and bad. health: 5 - 10*1 = -5
            ],
            dtype=np.int8
        )

        ar___bad = np.array([0, 0, 0, 1, 0])
        ar__good = np.array([1, 0, 1, 0, 0])
        ar_fatal = np.array([0, 1, 0, 0, 1])

        health = on_split_locuses(pop, ar__good, ar___bad, ar_fatal)

        assert_array_equal(
            health,
            np.array([5, 0.1, -5, 5, -5], dtype=np.float32)
        )
