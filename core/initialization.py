import numpy as np


def all_zeros(num_ind, num_locuses, *args, **kwargs):
    return np.zeros((num_ind, num_locuses), dtype=np.int8)


def uniform(num_ind, num_locuses, *args, **kwargs):
    return np.random.randint(0, 2, (num_ind, num_locuses), dtype=np.int8)


def normal_with_locuses(num_ind, num_locuses, good, *args, **kwargs):
    pop = np.zeros((num_ind, num_locuses), dtype=np.int8)
    healthes = np.round(np.abs(np.random.normal(0, 1, num_ind)))

    for i in range(num_ind):
        count = 0
        while count < healthes[i]:
            ind = np.random.randint(0, num_locuses)
            while good[ind] != 0:
                ind = np.random.randint(0, num_locuses)

            pop[i][ind] = 1
            count += 1

    return pop
