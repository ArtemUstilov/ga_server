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
        probabilities = values/sum_val
    else:
        probabilities = 1/len(values)

    def get_indiv(ind):
        return population[ind]

    random_indexes = np.random.choice(np.arange(len(population)), final_population_size, p=probabilities)
    return np.array(list(map(get_indiv, random_indexes)))
    # return population[random_indexes]


def tournament(population, values, final_population_size, tournament_size):
    res = []
    for i in range(final_population_size):
        randomIndexes = np.random.choice(len(population), tournament_size, replace=False)
        selectedValues = np.take(values, randomIndexes)
        selectedIndividuals = np.take(population, randomIndexes, axis=0)
        maxIndex = np.argmax(selectedValues)
        res.append(selectedIndividuals[maxIndex])
    return res
