import numpy as np


def hamming_distance_between(ind1: np.ndarray, ind2: np.ndarray) -> int:
    """

    :param ind1:
    :param ind2:
    :return: hamming distance between these inds
    """
    return (ind1 ^ ind2).sum(axis=0)
