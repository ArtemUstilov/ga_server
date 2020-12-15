import numpy as np


def crossover(pop: np.ndarray, pc: float) -> np.ndarray:
    """
    Performs in place crossover on giver population

    :param pop: population
    :param pc: value of probability [0, 1] for each pair to have crossover

    :return: modified population
    """

    N = pop.shape[0]
    L = pop.shape[1]
    assert N % 2 == 0, "N must be even number"

    inds_a = np.zeros(N, dtype=bool)

    # Divide population into two groups
    inds_a[np.random.choice(N, N // 2, replace=False)] = True
    inds_b = ~inds_a

    # Generate cross points for each pair
    cross_points = np.random.randint(0, L, N // 2)

    # Decide for each pair whether we perform crossover
    use_crossover = np.random.random(N // 2) < pc

    # Prepare indices and cross points only for pairs that are selected for crossover
    prep_a = np.argwhere(inds_a).reshape(-1)[use_crossover]
    prep_b = np.argwhere(inds_b).reshape(-1)[use_crossover]
    prep_points = cross_points[use_crossover]

    for i in range(len(prep_points)):
        a = prep_a[i]
        b = prep_b[i]
        point = prep_points[i]

        tmp = pop[a].copy()
        # Crossover
        pop[a, point:], pop[b, point:] = pop[b, point:], tmp[point:]

    return pop
