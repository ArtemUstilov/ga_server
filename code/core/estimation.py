import numpy as np


def hamming_distance(popul) -> np.ndarray:
    return popul.sum(1, dtype=np.int32)


def inverted_hamming_distance(popul, *args, **kwargs):
    l = popul.shape[1]
    return l - popul.sum(1, dtype=np.int32)


def const(popul, *args, **kwargs):
    return np.zeros(popul.shape[0], dtype=np.int32) + popul.shape[1]


def sigma_2(popul, *args, **kwargs):
    l = popul.shape[1]
    ks = l - popul.sum(1)

    return l - ks + ks * 2


def sigma_4(popul, *args, **kwargs):
    l = popul.shape[1]
    ks = l - popul.sum(1)

    return l - ks + ks * 4


def sigma_10(popul, *args, **kwargs):
    l = popul.shape[1]
    ks = l - popul.sum(1)

    return l - ks + ks * 10
