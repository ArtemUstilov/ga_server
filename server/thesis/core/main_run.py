import math
import json

import uuid
from threading import Thread

import numpy as np
from psycopg2.extras import execute_values

from .database import open_db_cursor
from .mutation import mutate
from .draw_plot_analysis import fill_chart
from . import constants

from .utils import pairwise_hamming_distribution, ideal_hamming_distribution, \
    wild_type_hamming_distribution, locus_roles_polymorphous


def run(cursor, conn, run_id, uniq_id, l, n, px, estim, init, sel_type, size_pop_type):
    cursor.execute(
        f"SELECT good_locuses, bad_locuses, lethal_locuses  FROM locus_helper WHERE l={l}")
    row = cursor.fetchone()
    kwargs = {
        'good': np.array(row[0], dtype=np.int8),
        'bad': np.array(row[1], dtype=np.int8),
        'lethal': np.array(row[2], dtype=np.int8)
    }

    estimation = constants.ESTIM_MAP[estim]
    initialization = constants.INIT_MAP[init]
    selection = constants.SELECTION_MAP[sel_type]
    size_pop = constants.SIZE_POP[size_pop_type]
    pop = initialization(size_pop(0, 1), l, **kwargs)
    health = estimation(pop, **kwargs)

    store_in_db(cursor, conn, uniq_id, pop, health, health.mean(), 0, False, **kwargs)

    succ = False
    for i in range(1, constants.N_IT):
        if i % 50 == 0:
            print(i)
        pop = selection(pop, health, size_pop(i, len(pop)))
        pop = mutate(pop, px)
        health = estimation(pop, **kwargs)
        mean_health = health.mean()

        if i == constants.N_IT - 1:
            store_in_db(cursor, conn, uniq_id, pop, health, mean_health, i, True, **kwargs)
            fill_chart(uniq_id)
            break
        if i % 100 == 0:
            store_in_db(cursor, conn, uniq_id, pop, health, mean_health, i, False, **kwargs)

    return succ


def store_settings(cursor, conn, run_id, L,
                   init, estim, sel_type, size_pop_type):
    uniq_id = uuid.uuid4()

    data = (
        str(uniq_id),
        init,
        estim,
        sel_type,
        size_pop_type,
        L,  # L
        run_id
    )

    sql_insert_settings = f"""
            INSERT INTO ga_run_settings ({','.join(constants.cols_settings)})
            VALUES %s;
            """

    execute_values(cursor, sql_insert_settings, [data])

    conn.commit()

    return uniq_id


def store_in_db(cursor, conn, uniq_id, pop, health, mean_health, it, last_iter, good, bad, lethal):
    ham_dist = pairwise_hamming_distribution(pop)
    if ham_dist.sum() == 0:
        ham_dist_p = ham_dist
    else:
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
        pop.shape[0],  # N
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

        ham_dist.argmin(),
        ham_dist.argmax(),
        ideal_dist.argmin(),
        ideal_dist.argmax(),
        wild_dist.argmin(),
        wild_dist.argmax(),

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

        locus_roles_polymorphous(pop, good),
        str(uniq_id),
        last_iter
    )

    sql_insert_info = f"""
        INSERT INTO ga_run_info ({','.join(constants.cols_info)})
        VALUES %s;
        """

    execute_values(cursor, sql_insert_info, [data])

    conn.commit()


def start(inits, estims, ls, sel_types, pxs, types, run_id_n=5):
    with open_db_cursor(constants.conn_str) as (cursor, conn):
        for init in inits:
            for estim in estims:
                for sel_type in sel_types:
                    for size_type in types:
                        n = constants.N_POP[size_type]
                        for l in ls:
                            print((init, estim, l, n, sel_type))
                            px = pxs[(l, n, sel_type)]
                            for i in range(run_id_n):
                                run(
                                    cursor,
                                    conn,
                                    i,
                                    l,
                                    n,
                                    px,
                                    estim,
                                    init,
                                    sel_type,
                                    size_type
                                )


def start_one(init, estim, l, sel_type, px, size_type, runs):
    with open_db_cursor(constants.conn_str) as (cursor, conn):
        n = constants.N_POP[size_type]

        ids = []

        for i in range(runs):
            ids.append(store_settings(cursor, conn, i, l, init, estim, sel_type, size_type))

        print((init, estim, l, n, sel_type))

        t = Thread(target=one_run, args=(init, estim, l, n, sel_type, px, size_type, ids))
        t.start()

        return ids


def one_run(init, estim, l, n, sel_type, px, size_type, ids):
    with open_db_cursor(constants.conn_str) as (cursor, conn):
        # init same population for all runs
        # get px from px_info depends on passed settings

        for i in range(len(ids)):
            run(
                cursor,
                conn,
                i,
                ids[i],
                l,
                n,
                px,
                estim,
                init,
                sel_type,
                size_type
            )


def info_about_last(run_id):
    with open_db_cursor(constants.conn_str) as (cursor, conn):
        cursor.execute(f"SELECT * FROM ga_run_info "
                       f"where ga_run_settings_id = '{run_id}' and last_iter=true")
        finish = len(cursor.fetchall()) > 0
        cursor.execute(f"SELECT max(iteration) FROM ga_run_info "
                       f"where ga_run_settings_id = '{run_id}'")
        res = {'finish': finish, 'iter': cursor.fetchone()[0]}
        return json.dumps(res)


def available_runs():
    with open_db_cursor(constants.conn_str) as (cursor, conn):
        cursor.execute(f"SELECT * FROM ga_run_settings order by created_date desc limit 5")

        rows = [x for x in cursor]
        cols = [x[0] for x in cursor.description]

        runs = []
        for row in rows:
            run = {}
            for prop, val in zip(cols, row):
                if prop == 'created_date' or prop == 'chart':
                    continue
                if isinstance(val, str):
                    val = val.strip()
                run[prop] = val
            runs.append(run)

        runs_json = json.dumps(runs)

        return runs_json


def get_chart(run_id):
    with open_db_cursor(constants.conn_str) as (cursor, conn):
        cursor.execute(f"SELECT chart FROM ga_run_settings "
                       f"where id = '{run_id}'")

        res = {'data': cursor.fetchone()[0].tobytes().decode("utf-8")}
        return json.dumps(res)


def get_info(run_id):
    with open_db_cursor(constants.conn_str) as (cursor, conn):
        cursor.execute(f"SELECT * FROM ga_run_info gi INNER JOIN ga_run_settings gs on gi.ga_run_settings_id=gs.id "
                       f"where ga_run_settings_id = '{run_id}'")

        rows = [x for x in cursor]
        cols = [x[0] for x in cursor.description]

        iterations = []
        for row in rows:
            iteration = {}
            for prop, val in zip(cols, row):
                if prop == 'created_date' or prop == 'chart':
                    continue
                if isinstance(val, str):
                    val = val.strip()
                iteration[prop] = val
            iterations.append(iteration)

        iterations_json = json.dumps(iterations)

        return iterations_json
