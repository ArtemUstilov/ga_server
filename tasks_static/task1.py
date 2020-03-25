import math
import pandas as pd

import numpy as np

from database import engine
from tasks_static.files import write_file
from core.initialization import uniform
from core.estimation import hamming_distance
from core.mutation import mutate
from core.selection import roulette
from utils import (
    pairwise_hamming_distribution,
    ideal_hamming_distribution,
    wild_type_hamming_distribution,
)

EPS = 0.1
N_IT = 20000


def run(run_id, l, n, px):
    hist_file = get_empty_histogram(20000, l)
    mean_health_ar = np.zeros(N_IT)

    pop = uniform(n, l)
    health = l - hamming_distance(pop)
    mean_health_ar[0] = health.mean()
    append_to_histogram(hist_file, pop, mean_health_ar[0], health.max(), 0)
    stop = N_IT
    for i in range(1, N_IT):
        pop = roulette(pop, health, n)
        pop = mutate(pop, px)
        health = l - hamming_distance(pop)
        mean_health = health.mean()
        append_to_histogram(hist_file, pop, mean_health, health.max(), i)

        mean_health_ar[i] = mean_health
        if converges(mean_health_ar, i):
            stop = i
            break

        if i % 100 == 0:
            print('Iteration:', i)

    df = pd.DataFrame(hist_file[:stop+2], columns=get_cols(l))
    name = f'task1\\task1_id_{run_id}_L_{l}_N_{n}_px_{px:.4f}'

    print('saving')
    df.to_sql(name, engine)
    print('to_db')
    write_file(name, df)
    print('to_file')


def get_empty_histogram(its, l):
    return np.zeros((its, len(get_cols(l))), dtype=np.float64)


def append_to_histogram(hist, pop, mean_health, best_health, it):
    num_ind = pop.shape[0]
    hist[it, 0] = it  # N of iteration
    hist[it, 1] = num_ind  # N of inds

    ham_dist = pairwise_hamming_distribution(pop)
    ideal_dist = ideal_hamming_distribution(pop)
    wild_dist = wild_type_hamming_distribution(pop)

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
    hist[it, i+4] = abs(pop.shape[1] - mean_health)  # Difference between best health and average
    hist[it, i+5] = abs(pop.shape[1] - best_health)  # mean health


def converges(mean_health_ar, it):
    return (
        # TODO remake with counter
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
        'Mean_health',
        'Mean_health_diff_0',
        'Best_health_diff_0',
    ]
    return cols


if __name__ == '__main__':
    for l in [5, 20, 80, 100, 200]:
        px = 1 / (10 * l)
        for n in [10, 100, 200]:
            for i in range(10):
                print(f'L={l} N={n} Run ID={i}. pm=Px=1/(10*l)')
                run(i, l, n, px)
