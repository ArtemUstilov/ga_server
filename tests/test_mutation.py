from decimal import Decimal
from unittest import TestCase, mock
from numpy.testing import assert_array_equal

import numpy as np

from mutation import mutate


class TestMutate(TestCase):

    def test_empty(self):
        pop = np.zeros((5, 5), dtype=np.int8)
        matrix = np.array([
            [1, 0, 0, 0, 0],
            [1, 0, 1, 0, 0],
            [0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1],
        ])
        with mock.patch('mutation.np.random.choice',
                        mock.MagicMock(return_value=matrix)):
            pop = mutate(pop, Decimal('0.1'))

        assert_array_equal(pop, matrix)

    def test_custom(self):
        pop = np.array([
            [1, 0, 1],
            [1, 1, 0],
            [1, 1, 1],
        ], dtype=np.int8)
        matrix = np.array([
            [0, 0, 1],
            [0, 0, 0],
            [1, 1, 1],
        ], dtype=np.int8)
        with mock.patch('mutation.np.random.choice',
                        mock.MagicMock(return_value=matrix)):
            pop = mutate(pop, Decimal('0.1'))

        assert_array_equal(pop, np.array([
            [1, 0, 0],
            [1, 1, 0],
            [0, 0, 0],
        ], dtype=np.int8))