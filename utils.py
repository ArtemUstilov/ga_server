import random
import numpy as np
from scipy import stats
import estimation

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


def mse(health):
    return health.std()


def average(health):
    return health.average()


def mean(health):
    return health.mean()


def mode(health):
    return stats.mode(health)


def mod_diff_best(health):
    # TODO find where to get optimal value
    opt = 0
    return abs(opt - health.max())


def mod_diff_average(health):
    # TODO find where to get optimal value
    opt = 0
    return abs(opt - average(health))


def get_wild_type(population):

    def get_max(x):
        return np.argmax(np.bincount(x))

    return np.array(list(map(get_max, population.swapaxes(0,1))))


def percent_polymorf_wild(population):
    return polymorf_wild(population)/population.shape[1]


def polymorf_wild(population):
    return estimation.hamming_distance(np.array([get_wild_type(population)]))[0]


def hamming_distances(population):
    return np.bincount(estimation.hamming_distance(population))


def pairwise_hamming_distribution(population):
    matrix = (population[:, None, :] != population).sum(2)
    np.fill_diagonal(matrix, -1)
    d = np.zeros(population.shape[1], dtype=np.int64)
    for i in range(len(d)):
        d[i] = (matrix == i).sum() / 2

    return d


def ideal_hamming_distribution(population):
    matrix = population.sum(1)
    d = np.zeros(population.shape[1], dtype=np.int64)

    for i in range(population.shape[1]):
        d[i] = (matrix == i).sum()

    return d
