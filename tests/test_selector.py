from unittest import TestCase
import numpy as np

from selection import roulette


class TestSelector(TestCase):

    def test_roulette(self):
        eps = 10.e-3
        res = 0
        pop = np.array([[1, 1, 1], [0, 0, 0]], dtype=np.int8)
        values = np.array([4, 1], dtype=np.int8)
        for _ in range(100000):
            res += roulette(pop, values, 1)[0][0]

        self.assertTrue(abs(res / 100000 - 1 / 5 * 4) < eps,
                        'It should return first individual in 80% cases')
        # res = 0
        # for i in range(100000):
        #     res += selection([[1, 1, 1], [0, 0, 0]], [1, 1], 1, ROULETTE)[0][0]
        # if abs(res / 100000 - 1 / 2) > E:
        #     raise Exception('It should return first individual in 50% cases')
        # res = 0
        # for i in range(100000):
        #     res += selection([[1, 1, 1], [0, 0, 0]], [4, 0], 1, ROULETTE)[0][0]
        # if res / 100000 != 1:
        #     raise Exception('It should return first individual in 100% cases')
