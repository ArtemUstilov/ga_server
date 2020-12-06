import numpy as np


def target_hamming_distribution(target, population):
    return (population ^ target).sum(axis=1).astype(np.int64)


def pairwise_hamming_distribution(population):
    matrix = (population[:, None, :] != population).sum(2)
    np.fill_diagonal(matrix, -1)
    d = np.zeros(population.shape[1], dtype=np.int64)
    for i in range(len(d)):
        d[i] = (matrix == i).sum() / 2

    return d
