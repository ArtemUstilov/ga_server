import numpy as np


def hamming_distance(population: np.ndarray) -> np.ndarray:
    return population.sum(1, dtype=np.int32)


def const(population: np.ndarray) -> np.ndarray:
    return np.zeros(population.shape[0], dtype=np.int32) + population.shape[1]


def on_split_locuses(population, good, bad, lethal) -> np.ndarray:
    """
    Provides an estimation as described in given task. Lethal locuses reduce health
    to 0.1. Bad locuses reduce health to (l - 10 k).

    ar_good, ar_bad, ar_lethal are arrays of length population.shape[0] of 0s and 1s.
    Indices with 1s represent locus type.
    1s in arrays cannot intersect and must cover all indices.
    """
    assert np.bitwise_and(np.bitwise_and(bad, lethal), good).sum() == 0,\
        "good, bad and fatal locuses cannot intersect"
    assert np.bitwise_or(np.bitwise_or(bad, lethal), good).sum() == population.shape[1], \
        "good, bad and fatal locuses must cover all indices"

    n = population.shape[0]
    l = population.shape[1]

    just_bad = np.bitwise_and(population, bad)
    bad_health = l - 10 * just_bad.sum(1)
    bad_inds = just_bad.max(1) * 3

    just_lethal = np.bitwise_and(population, lethal)
    lethal_inds = just_lethal.max(1) * 5

    inds_roles = bad_inds + lethal_inds
    p_health = np.zeros(n, dtype=np.float32)
    p_health[inds_roles == 0] = l
    p_health[inds_roles == 3] = bad_health[inds_roles == 3]
    p_health[inds_roles == 5] = 0.1
    p_health[inds_roles == 8] = 0.1

    return p_health
