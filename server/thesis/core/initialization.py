import numpy as np

from .utils import generate_locus_roles, GOOD


def all_zeros(num_ind, num_locuses, *args, **kwargs):
    return np.zeros((num_ind, num_locuses), dtype=np.int8)


def all_ones(num_ind, num_locuses, *args, **kwargs):
    return np.ones((num_ind, num_locuses), dtype=np.int8)


def half_zeros_half_ones(num_ind, num_locuses, random_state, *args, **kwargs):
    random = np.random
    if random_state:
        random = np.random.RandomState(random_state)

    arr = (np.concatenate(
        (np.zeros((int(num_ind / 2), num_locuses), dtype=np.int8),
         np.ones((int(num_ind / 2), num_locuses), dtype=np.int8)),
        axis=0))

    random.shuffle(arr)

    return arr


def all_1_one_0(num_ind, num_locuses, random_state, *args, **kwargs):
    random = np.random
    if random_state:
        random = np.random.RandomState(random_state)

    arr = (np.concatenate(
        (np.zeros((1, num_locuses), dtype=np.int8),
         np.ones((int(num_ind - 1), num_locuses), dtype=np.int8)),
        axis=0))

    random.shuffle(arr)

    return arr


def uniform(num_ind, num_locuses, *args, **kwargs):
    return np.random.randint(0, 2, (num_ind, num_locuses), dtype=np.int8)


def normal(num_ind, num_locuses,random_state,  *args, **kwargs):
    random = np.random
    if random_state:
        random = np.random.RandomState(random_state)

    pop = random.choice([0,1], (num_ind,num_locuses), p=[0.5, 0.5])

    return pop


def normal_with_ideal(num_ind, num_locuses,random_state, *args, **kwargs):
    random = np.random
    if random_state:
        random = np.random.RandomState(random_state)

    pop = random.choice([0,1], (num_ind,num_locuses), p=[0.5, 0.5])
    pop[0] = np.zeros(num_locuses)
    for i in range(1, pop.shape[0]):
        if pop[i].sum() == 0:
            pop[i] = random.choice([0,1], num_locuses, p=[0.5, 0.5])

    return pop


def normal_with_locuses(num_ind, num_locuses, *args, **kwargs):
    ar = generate_locus_roles(num_ind)
    good = list(ar == GOOD)

    pop = np.zeros((num_ind, num_locuses), dtype=np.int8)

    for i in range(num_ind):
        count = 0
        health = int(abs(np.random.normal()))
        while count < health:
            ind = np.random.randint(0, num_locuses)
            while good[ind] != 0 or pop[i][ind] == 1:
                ind = np.random.randint(0, num_locuses)

            pop[i][ind] = 1
            count += 1

    return pop
