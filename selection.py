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

    def getIndividual(p, v, val):
        acc = v[0]
        ind = 0
        while (acc < val):
            ind += 1
            acc += v[ind]
        return p[ind]

    res = []
    val_sum = np.sum(values)
    for x in range(final_population_size):
        res.append(getIndividual(population, values, random.uniform(0, val_sum)))
    return np.array(res, dtype=np.int8)
