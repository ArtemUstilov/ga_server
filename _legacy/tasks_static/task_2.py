import math

import numpy as np
from psycopg2.extras import execute_values

from server.thesis.core.database import open_db_cursor
from server.thesis.core.estimation import const as all_l, on_split_locuses
from server.thesis.core import all_zeros as all_0, normal_with_locuses as normal
from server.thesis.core import mutate
from server.thesis.core import roulette as rws, tournament_2, tournament_4, tournament_12
from server.thesis.core import pairwise_hamming_distribution, ideal_hamming_distribution, \
    wild_type_hamming_distribution

EPS = 0.0001
N_IT = 20000

INIT_MAP = {
    'all_0': all_0,
    'normal': normal,
}

ESTIM_MAP = {
    'all_l': all_l,
    'on_split_locuses': on_split_locuses,
}

SELECTION_MAP = {
    'rws': rws,
    'tournament_2': tournament_2,
    'tournament_4': tournament_4,
    'tournament_12': tournament_12,
}


def run(cursor, conn, run_id, l, n, px, sql_script, estim, init, sel_type):
    cursor.execute(
        f"SELECT good_locuses, bad_locuses, lethal_locuses  FROM locus_helper WHERE l={l}")
    row = cursor.fetchone()

    kwargs = {
        'good': np.array(row[0], dtype=np.int8),
        'bad': np.array(row[1], dtype=np.int8),
        'lethal': np.array(row[2], dtype=np.int8)
    }

    estimation = ESTIM_MAP[estim]
    initialization = INIT_MAP[init]
    selection = SELECTION_MAP[sel_type]

    pop = initialization(n, l, **kwargs)
    health = estimation(pop, **kwargs)

    store_in_db(cursor, conn, sql_script, run_id, pop, health, health.mean(), 0, init, estim,
                sel_type)
    succ = False
    for i in range(1, N_IT):
        pop = selection(pop, health, n)
        pop = mutate(pop, px)
        health = estimation(pop, **kwargs)
        print((health==0.1).sum())
        mean_health = health.mean()
        # store_in_db(cursor, conn, sql_script, run_id, pop, health, mean_health, i,
        #             init, estim, sel_type)

    return succ


def store_in_db(cursor, conn, sql_script, run_id, pop, health, mean_health, it,
                init, estim, sel_type):
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
        init,
        estim,
        sel_type,
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

        ham_dist.min(),
        ham_dist.max(),
        ideal_dist.min(),
        ideal_dist.max(),
        wild_dist.min(),
        wild_dist.max(),

        ham_std / ham_e_val if ham_e_val != 0 else None,  # variance coef ham
        ideal_std / ideal_e_val if ideal_e_val != 0 else None,  # variance coef ideal
        wild_std / wild_e_val if wild_e_val != 0 else None,  # variance coef wild

        list(np.argwhere(ham_dist == ham_dist.max()).reshape(-1)),  # mode hamming pairwise
        list(np.argwhere(ideal_dist == ideal_dist.max()).reshape(-1)),  # mode ideal
        list(np.argwhere(wild_dist == wild_dist.max()).reshape(-1)),  # mode wild type

        list(health),
        mean_health,
        abs(pop.shape[1] - mean_health),  # Difference between mean health and average
        abs(pop.shape[1] - health.max()),  # Difference between best health and average
    )

    execute_values(cursor, sql_script, [data])
    conn.commit()


cols = [
    'init',
    'estim',
    'sel_type',
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

    'min_pair',
    'max_pair',
    'min_ideal',
    'max_ideal',
    'min_wild',
    'max_wild',

    'variance_coef_pair',
    'variance_coef_ideal',
    'variance_coef_wild',

    'mode_pair',
    'mode_ideal',
    'mode_wild',

    'health',
    'mean_health',
    'mean_health_diff_0',
    'best_health_diff_0',
]


def start(conn_str, table_name, inits, estims, ls, ns, sel_types, pxs, run_ids):
    sql_insert = f"""
    INSERT INTO {table_name} ({','.join(cols)})
    VALUES %s;
    """

    with open_db_cursor(conn_str) as (cursor, conn):
        for init in inits:
            for estim in estims:
                for sel_type in sel_types:
                    for l in ls:
                        for n in ns:
                            print((init, estim, l, n, sel_type))
                            px = pxs[(l, n, sel_type)]
                            for i in run_ids:
                                run(
                                    cursor,
                                    conn,
                                    i,
                                    l,
                                    n,
                                    px,
                                    sql_insert,
                                    estim,
                                    init,
                                    sel_type
                                )
