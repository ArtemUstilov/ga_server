import random
import numpy as np

GOOD_INITIAL_PERCENT = 13.5
GOOD_OTHERS_PERCENT = 24.5
BAD_PERCENT = 2.32
LETHAL_PERCENT = 100 - GOOD_INITIAL_PERCENT - GOOD_OTHERS_PERCENT - BAD_PERCENT

GOOD = 1
BAD = 2
LETHAL = 3


def generate_locus_roles(size: int) -> np.ndarray:
    """
    Randomly (according to constants given in course tasks) predetermine
    which mutations will be fatal or patalogic.

    :param size: l param
    """

    roles = np.zeros(size)
    good_initial = round(size * GOOD_INITIAL_PERCENT / 100)
    good_others = round(size * GOOD_OTHERS_PERCENT / 100)
    bad = round(size * BAD_PERCENT / 100)

    roles[:good_initial] = GOOD
    tail = range(good_initial, size)
    good_inds = random.sample(list(tail), good_others)
    roles[good_inds] = GOOD
    bad_inds = random.sample(set(tail).difference(set(good_inds)), bad)
    roles[bad_inds] = BAD
    lethal_inds = list(set(tail).difference(good_inds).difference(bad_inds))
    roles[lethal_inds] = LETHAL
    return roles
