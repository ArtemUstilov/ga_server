import numpy as np


def hamming_distance(population: np.ndarray, *args, **kwargs) -> np.ndarray:
    l = population.shape[1]
    return l - population.sum(1, dtype=np.int32)


def inverted_hamming_distance(population: np.ndarray, *args, **kwargs) -> np.ndarray:
    return population.sum(1, dtype=np.int32)


def const(population: np.ndarray, *args, **kwargs) -> np.ndarray:
    return np.zeros(population.shape[0], dtype=np.int32) + population.shape[1]


def two_const(population: np.ndarray,  sigma, const_1, const_2, **kwargs) -> np.ndarray:
    res = np.array([])
    for x in population:
        if x.sum() == len(x):
            res = np.append(res, int(const_1))
        else:
            res = np.append(res, int(const_2))

    return res


def sigma(population: np.ndarray,  sigma, const_1, const_2, **kwargs) -> np.ndarray:
    l = population.shape[1]
    ks = l - population.sum(1)

    return l - ks + ks * int(sigma)

