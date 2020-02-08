import math

import numpy as np
from psycopg2.extras import execute_values

from estimation import hamming_distance
from initialization import uniform
from mutation import mutate
from selection import roulette
from utils import pairwise_hamming_distribution, ideal_hamming_distribution, \
    wild_type_hamming_distribution

EPS = 0.0001
N_IT = 20000


def run(cursor, conn, run_id, l, n, px, sql_script):
    last_counter = 0

    pop = uniform(n, l)
    health = l - hamming_distance(pop)

    store_in_db(cursor, conn, sql_script, run_id, pop, health, health.mean(), 0)
    last_mean_health = health.mean()
    succ = False
    for i in range(1, N_IT):
        pop = roulette(pop, health, n)
        pop = mutate(pop, px)
        health = l - hamming_distance(pop)
        mean_health = health.mean()
        store_in_db(cursor, conn, sql_script, run_id, pop, health, mean_health, i)

        if abs(last_mean_health - mean_health) < EPS:
            last_counter += 1
        else:
            last_counter = 0

        if last_counter >= 10:
            succ = True
            break

        last_mean_health = mean_health

        if i % 500 == 0:
            print('Iteration:', i)

    return succ


def store_in_db(cursor, conn, sql_script, run_id, pop, health, mean_health, it):
    ham_dist = pairwise_hamming_distribution(pop)
    ham_dist_p = (ham_dist / ham_dist.sum())
    ideal_dist = ideal_hamming_distribution(pop)
    ideal_dist_p = (ideal_dist / ideal_dist.sum())
    wild_dist = wild_type_hamming_distribution(pop)
    wild_dist_p = (wild_dist / wild_dist.sum())

    ham_e_val = np.dot(np.arange(ham_dist.shape[0]), ham_dist_p)
    ham_e_val_sqr = np.dot(np.arange(ham_dist.shape[0]) ** 2, ham_dist_p)
    ham_std = math.sqrt(ham_e_val_sqr - ham_e_val ** 2)

    ideal_e_val = np.dot(np.arange(ideal_dist.shape[0]), ideal_dist_p)
    ideal_e_val_sqr = np.dot(np.arange(ideal_dist.shape[0]) ** 2, ideal_dist_p)
    ideal_std = math.sqrt(ideal_e_val_sqr - ideal_e_val ** 2)

    wild_e_val = np.dot(np.arange(wild_dist.shape[0]), wild_dist_p)
    wild_e_val_sqr = np.dot(np.arange(wild_dist.shape[0]) ** 2, wild_dist_p)
    wild_std = math.sqrt(wild_e_val_sqr - wild_e_val ** 2)

    data = (
        pop.shape[1],  # L
        pop.shape[0],  # N
        run_id,
        it,  # iteration

        list(ham_dist_p),  # pairwise_hamming_distribution_p
        list(ham_dist),  # pairwise_hamming_distribution_abs
        list(ideal_dist_p),  # ideal_hamming_distribution_p
        list(ideal_dist),  # ideal_hamming_distribution_abs
        list(wild_dist_p),  # wild_type_hamming_distribution_p
        list(wild_dist),  # wild_type_hamming_distribution_abs

        ham_e_val,
        ham_std,
        ideal_e_val,
        ideal_std,
        wild_e_val,
        wild_std,

        ham_dist.argmax(),  # mode hamming pairwise
        ideal_dist.argmax(),  # mode ideal
        wild_dist.argmax(),  # mode wild type

        list(health),
        mean_health,
        abs(pop.shape[1] - mean_health),  # Difference between mean health and average
        abs(pop.shape[1] - health.max()),  # Difference between best health and average
    )

    execute_values(cursor, sql_script, [data])
    conn.commit()


cols = [
    'L',
    'N',
    'run_id',
    'iteration',

    'pairwise_hamming_distribution_p',
    'pairwise_hamming_distribution_abs',
    'ideal_hamming_distribution_p',
    'ideal_hamming_distribution_abs',
    'wild_type_hamming_distribution_p',
    'wild_type_hamming_distribution_abs',

    'expected_value_pair',
    'std_pair',
    'expected_value_ideal',
    'std_ideal',
    'expected_value_wild',
    'std_wild',

    'mode_pair',
    'mode_ideal',
    'mode_wild',

    'health',
    'mean_health',
    'mean_health_diff_0',
    'best_health_diff_0',
]
