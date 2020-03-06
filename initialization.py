import numpy as np


def all_zeros(num_ind, num_locuses, *args, **kwargs):
    return np.zeros((num_ind, num_locuses), dtype=np.int8)


def uniform(num_ind, num_locuses):
    return np.random.randint(0, 2, (num_ind, num_locuses), dtype=np.int8)


def split_population(num_ind, num_locuses, pure_p, impure_p):
    assert pure_p + impure_p == 100, "Pure and impure individuals" \
                                 " together make 100% of population "
    impure_n = round(impure_p / 100.0 * num_ind)
    pure_n = num_ind - impure_n

    impure = np.random.randint(2, size=(impure_n, num_locuses), dtype=np.int8)
    pure = np.zeros((pure_n, num_locuses), dtype=np.int8)

    res = np.concatenate([impure, pure])
    np.random.shuffle(res)
    return res


def init_good_by_normal_distribution(num_ind, num_locuses, good,  *args, **kwargs):
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
