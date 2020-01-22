import math
import pandas as pd

import numpy as np

from files import write_file
from initialization import uniform
from estimation import hamming_distance
from mutation import mutate
from selection import roulette
from utils import pairwise_hamming_distribution

EPS = 0.1
N_IT = 20000


def run(l, n, px):
    hist_file = get_empty_histogram(20000, l)
    mean_health_ar = np.zeros(N_IT)

    pop = uniform(n, l)
    health = l - hamming_distance(pop)
    mean_health_ar[0] = health.mean()
    append_to_histogram(hist_file, pop, mean_health_ar[0], 0)
    for i in range(1, N_IT):
        pop = roulette(pop, health, n)
        pop = mutate(pop, px)
        health = l - hamming_distance(pop)
        mean_health = health.mean()
        append_to_histogram(hist_file, pop, mean_health, i)

        mean_health_ar[i] = mean_health
        if converges(mean_health_ar, i):
            break

        if i % 100 == 0:
            print('Iteration:', i)

    df = pd.DataFrame(hist_file, columns=get_cols(l))
    write_file(f'task1_L_{l}_N_{n}_px_{px:.4f}', df)


def get_empty_histogram(its, l):
    return np.zeros((its, len(get_cols(l))), dtype=np.float64)


def append_to_histogram(hist, pop, mean_health, it):
    num_ind = pop.shape[0]
    hist[it, 0] = it  # N of iteration
    hist[it, 1] = num_ind  # N of inds
    ham_dist = pairwise_hamming_distribution(pop)
    s = ham_dist.sum()
    e = 0
    e2 = 0
    for i in range(2, pop.shape[1] + 2):
        pi = ham_dist[i - 2] / s
        hist[it, i] = pi  # probability distribution
        e += pi * i
        e2 += pi * i * i
    i = pop.shape[1] + 2
    hist[it, i] = e  # expected value
    hist[it, i+1] = math.sqrt(e2 - e ** 2)  # std
    hist[it, i+2] = ham_dist.argmax()  # mode
    hist[it, i+3] = mean_health  # mean health


def converges(mean_health_ar, it):
    return (
        it > 10 and
        abs(mean_health_ar[it-10] - mean_health_ar[it-9]) < EPS and
        abs(mean_health_ar[it-9] - mean_health_ar[it-8]) < EPS and
        abs(mean_health_ar[it-8] - mean_health_ar[it-7]) < EPS and
        abs(mean_health_ar[it-7] - mean_health_ar[it-6]) < EPS and
        abs(mean_health_ar[it-6] - mean_health_ar[it-5]) < EPS and
        abs(mean_health_ar[it-5] - mean_health_ar[it-4]) < EPS and
        abs(mean_health_ar[it-4] - mean_health_ar[it-3]) < EPS and
        abs(mean_health_ar[it-3] - mean_health_ar[it-2]) < EPS and
        abs(mean_health_ar[it-2] - mean_health_ar[it-1]) < EPS and
        abs(mean_health_ar[it-1] - mean_health_ar[it]) < EPS
    )


def get_cols(l):
    cols = [
        'It',
        'Num_ind'
    ]
    cols += [
        f'D_{i}'
        for i in range(l)]
    cols += [
        'Expected_value',
        'Std',
        'Mode',
        'Mean_health'
    ]
    return cols


if __name__ == '__main__':
    run(50, 100, 0.001)
