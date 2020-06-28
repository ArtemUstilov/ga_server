import numpy as np


def hamming_distance(population: np.ndarray, *args, **kwargs) -> np.ndarray:
    return population.sum(1, dtype=np.int32)


def inverted_hamming_distance(population: np.ndarray, *args, **kwargs) -> np.ndarray:
    l = population.shape[1]
    return l - population.sum(1, dtype=np.int32)


def const(population: np.ndarray, *args, **kwargs) -> np.ndarray:
    return np.zeros(population.shape[0], dtype=np.int32) + population.shape[1]


def sigma_2(population: np.ndarray, *args, **kwargs) -> np.ndarray:
    l = population.shape[1]
    ks = l - population.sum(1)

    return l - ks + ks * 2


def sigma_4(population: np.ndarray, *args, **kwargs) -> np.ndarray:
    l = population.shape[1]
    ks = l - population.sum(1)

    return l - ks + ks * 4


def sigma_10(population: np.ndarray, *args, **kwargs) -> np.ndarray:
    l = population.shape[1]
    ks = l - population.sum(1)

    return l - ks + ks * 10
