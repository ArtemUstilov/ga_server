import numpy as np


def roulette(population, values, final_p_size):
    sum_v = values.sum()
    if sum_v != 0:
        probabilities = values / sum_v
    else:
        probabilities = 1 / len(values)

    random_indexes = np.random.choice(len(population), final_p_size, p=probabilities)
    return population[random_indexes]


def tournament_12(population, values, final_p_size):
    tours = np.random.choice(population.shape[0], (final_p_size, 12))
    tour_winner = np.argmax(values[tours], axis=1)

    return population[tours[np.arange(final_p_size), tour_winner]]


def tournament_4(population, values, final_p_size):
    tours = np.random.choice(population.shape[0], (final_p_size, 4))
    tour_winner = np.argmax(values[tours], axis=1)

    return population[tours[np.arange(final_p_size), tour_winner]]


def tournament_2(population, values, final_p_size):
    a1 = np.random.choice(population.shape[0], final_p_size)
    a2 = np.random.choice(population.shape[0], final_p_size)
    a3 = values[a1] > values[a2]

    return np.concatenate(
        [population[a1[a3]], population[a2[np.logical_not(a3)]]]
    )
