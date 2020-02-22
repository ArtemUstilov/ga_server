import numpy as np


def all_zeros(num_ind, num_locuses):
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


def split_population_spec(self):
    pass
