from decimal import Decimal

import numpy as np


def mutate(population: np.ndarray, px: Decimal):
    mutation_matrix = np.random.choice(
        a=2,
        size=population.shape,
        p=[Decimal('1')-px, px],
    ).astype(population.dtype)
    return np.bitwise_xor(population, mutation_matrix)
