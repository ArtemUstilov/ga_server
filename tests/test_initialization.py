from unittest import TestCase
from initialization import split_population


class TestSplitPopulation(TestCase):

    def test_100_percent(self):
        kwargs = {
            'num_ind': 10,
            'num_locuses': 7,
            'pure_p': 50,
            'impure_p': 0
        }

        self.assertRaises(AssertionError, split_population, **kwargs)

    def test_all_pure(self):
        pop = split_population(10, 5, 100, 0)
        self.assertEquals(pop.sum(), 0)
