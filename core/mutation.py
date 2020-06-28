import numpy as np


def mutate(population: np.ndarray, px: float) -> np.ndarray:
    population[np.random.rand(*population.shape) < px] ^= 1
    return population
