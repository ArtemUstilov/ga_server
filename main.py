from decimal import Decimal

from estimation import hamming_distance
from initialization import uniform
from mutation import mutate
from selection import roulette

if __name__ == '__main__':
    # Global parameters
    l = 8000
    N = 80000
    px = Decimal(1) / Decimal(10 * l)
    print(px)

    # 1. Initialization
    pop1 = uniform(N, l)

    for it in range(10000):
        print('it1:', it)
        # 2. Estimation
        health = hamming_distance(pop1)
        # print(pop1)

        # 3. Selection
        # pop1 = roulette(pop1, health, N)
        print('it2:', it)

        # 4. Mutation
        pop1 = mutate(pop1, px)
        print('it3:', it)
