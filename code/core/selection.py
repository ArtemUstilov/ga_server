import numpy as np


def roulette(population, values, final_p_size):
    prob = values / values.sum() if values.sum() != 0 else 1 / len(values)

    random_inds = np.random.choice(len(population), final_p_size, p=prob)
    return population[random_inds]


def tournament_12(population, values, final_p_size):
    tours = np.random.choice(population.shape[0], (final_p_size, 12))
    t_winner = np.argmax(values[tours], axis=1)

    return population[tours[np.arange(final_p_size), t_winner]]


def tournament_4(population, values, final_p_size):
    tours = np.random.choice(population.shape[0], (final_p_size, 4))
    t_winner = np.argmax(values[tours], axis=1)

    return population[tours[np.arange(final_p_size), t_winner]]


def tournament_2(popul, values, final_p_size):
    a1 = np.random.choice(popul.shape[0], final_p_size)
    a2 = np.random.choice(popul.shape[0], final_p_size)
    a3 = values[a1] > values[a2]

    return np.concatenate(
        [popul[a1[a3]], popul[a2[np.logical_not(a3)]]]
    )
