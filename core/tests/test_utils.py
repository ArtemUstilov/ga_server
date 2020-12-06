from unittest import TestCase
from old import utils
from old.utils import *


class TestGenerateLocusRoles(TestCase):

    def test_const_percents(self):
        size = 10000
        res = generate_locus_roles(size)
        self.assertEqual(
            sum(res == GOOD),
            round((GOOD_INITIAL_PERCENT + GOOD_OTHERS_PERCENT) * 100)
        )
        self.assertEqual(
            sum(res == BAD),
            round(BAD_PERCENT * 100)
        )
        self.assertEqual(
            sum(res == LETHAL),
            round(LETHAL_PERCENT * 100)
        )

    def test_custom_percents(self):
        size = 100
        utils.GOOD_INITIAL_PERCENT = 30
        utils.GOOD_OTHERS_PERCENT = 20
        utils.BAD_PERCENT = 5
        res = generate_locus_roles(size)
        self.assertEqual(sum(res == GOOD),  50)
        self.assertEqual(sum(res == BAD), 5)
        self.assertEqual(sum(res == LETHAL), 45)
