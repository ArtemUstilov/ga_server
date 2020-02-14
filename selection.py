import random

import numpy as np


# class Selector:
#
#     def __init__(self, population: Population, health: np.ndarray, final_size: int):
#         self._ar = population
#         self._health = health
#         self._final_size = final_size
#
#     def _get_individual(self, val):
#         acc = self._health[0]
#         ind = 0
#         while acc < val:
#             ind += 1
#             acc += self._health[ind]
#         return self._ar.get_individual(ind)
#
#     def roulette(self):
#         res = []
#         val_sum = np.sum(self._health)
#         for x in range(self._final_size):
#             res.append(self._get_individual(random.uniform(0, val_sum)))
#         return res
#
#     def tournament(self, t):
#         pass


def roulette(population, values, final_population_size):
    sum_val = values.sum()
    if sum_val != 0:
        probabilities = values / sum_val
    else:
        probabilities = 1 / len(values)

    random_indexes = np.random.choice(len(population), final_population_size, p=probabilities)
    # return np.array(list(map(get_indiv, random_indexes)))
    return population[random_indexes]


def tournament(population, values, final_population_size, tournament_size):
    def take_best_index(*args):
        random_indexes = np.random.choice(len(population), tournament_size, replace=False)
        max_index = max(random_indexes, key=lambda i: values[i])
        return max_index

    inds = np.vectorize(take_best_index)(np.zeros(final_population_size))

    return population[inds]


def tournament_v2(population, values, final_population_size, tournament_size):
    def take_best_index(*args):
        random_indexes = np.random.choice(len(population), len(population) - tournament_size)
        selected_values = values[random_indexes]
        max_index = random_indexes[selected_values.argmax()]
        return max_index

    inds = np.vectorize(take_best_index)(np.zeros(final_population_size))

    return population[inds]


def tournament_2(population, values, final_population_size):
    a1 = np.random.choice(population.shape[0], final_population_size)
    a2 = np.random.choice(population.shape[0], final_population_size)

    a3 = values[a1] > values[a2]

    return np.concatenate([population[a1[a3]], population[a2[np.logical_not(a3)]]])


def tournament_4(population, values, final_population_size):
    tours = np.random.choice(population.shape[0], (final_population_size, 4))

    tour_winner = np.argmax(values[tours], axis=1)

    return population[tours[np.arange(final_population_size), tour_winner]]


def tournament_12(population, values, final_population_size):
    tours = np.random.choice(population.shape[0], (final_population_size, 12))

    tour_winner = np.argmax(values[tours], axis=1)

    return population[tours[np.arange(final_population_size), tour_winner]]
