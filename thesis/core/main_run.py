import math
import json
import uuid
from scipy.stats import variation
from threading import Thread

from django.core.serializers.json import DjangoJSONEncoder

import numpy as np
from psycopg2.extras import execute_values

from .database import open_db_cursor
from .estimation import hamming_distance
from . import constants

from .utils import pairwise_hamming_distribution, ideal_hamming_distribution, \
    wild_type_hamming_distribution


def run(cursor, conn, run_id, uniq_id, l, n, px, estim, pop, sel_type, use_mutation, save_pair, sigma, const_1,
        const_2, sel_param1, sel_param2, maxN, stop_confluence):
    kwargs = {
        'sigma': sigma,
        'const_1': const_1,
        'const_2': const_2,
        'sel_param1': sel_param1,
        'sel_param2': sel_param2,
        'G': maxN,
        'iter': 0,
        'sel_param3': 0,
    }

    estimation = constants.ESTIM_MAP[estim]
    selection = constants.SELECTION_MAP[sel_type]

    health = estimation(pop, **kwargs)

    store_in_db(cursor, conn, uniq_id, pop, health, health.mean(), 0, False, save_pair, len(health), health.mean(),
                health, hamming_distance(pop, **kwargs),
                **kwargs)

    succ = False

    mean_health = health.mean()
    all_health_worst = np.zeros(maxN + 1)
    all_health_worst[0] = health.min()
    for i in range(1, maxN):
        kwargs['iter'] = i
        kwargs['sel_param3'] = np.array(all_health_worst[0:i]).min()

        pop, taken_to_next = selection(pop, health, **kwargs)

        prev_health = health
        health = estimation(pop, **kwargs)
        all_health_worst[i + 1] = health.min()
        prev_mean_health = mean_health
        mean_health = health.mean()

        confluence = pop.sum() == 0 or pop.sum() == pop.shape[0] * pop.shape[1]
        last_iter = i == maxN - 1
        store_in_db(cursor, conn, uniq_id, pop, health, mean_health, i, confluence or last_iter, save_pair,
                    taken_to_next, prev_mean_health, prev_health, hamming_distance(pop, **kwargs), **kwargs)

        if confluence:
            break

    return succ


def store_settings(cursor, conn, run_id, init, estim, sel_type, l, n, px, use_mutation, const_1, const_2, sigma,
                   sel_param1, sel_param2, title):
    uniq_id = uuid.uuid4()

    data = (
        str(uniq_id),
        init,
        estim,
        sel_type,
        l,  # L
        n,
        px,
        use_mutation,
        run_id,
        const_1, const_2, sigma, sel_param1, sel_param2, title
    )

    sql_insert_settings = f"""
            INSERT INTO ga_run_settings ({','.join(constants.cols_settings)})
            VALUES %s;
            """

    execute_values(cursor, sql_insert_settings, [data])

    conn.commit()

    return uniq_id


def store_in_db(cursor, conn, uniq_id, pop, health, mean_health, it, last_iter, save_pair, taken_to_next,
                prev_mean_health, prev_health, genotype, **kwargs):
    if not save_pair:
        data = (
            pop.shape[0],  # N
            it,  # iteration

            None,
            None,
            None,
            None,
            None,
            None,

            None,
            None,
            None,
            None,
            None,
            None,

            None,
            None,
            None,
            None,
            None,
            None,

            None,
            None,
            None,
            None,
            None,
            None,

            list(health),
            mean_health,
            abs(pop.shape[1] - mean_health),  # Difference between mean health and average
            abs(pop.shape[1] - health.max()),  # Difference between best health and average

            str(uniq_id),
            last_iter,
            health.max(),
            health[health == health.max()].shape[0],
            taken_to_next,
            mean_health - prev_mean_health,
            0 if np.std(prev_health) == 0 else ((mean_health - prev_mean_health) / np.std(prev_health)),
            health[health == health.max()].shape[0] / prev_health[prev_health == prev_health.max()].shape[0],
            list(genotype)
        )
    else:
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

            str(uniq_id),
            last_iter,
            health.max(),
            health[health == health.max()].shape[0],
            taken_to_next,
            mean_health - prev_mean_health,
            (mean_health - prev_mean_health) / np.std(prev_health),
            health[health == health.max()].shape[0] / prev_health[prev_health == prev_health.max()].shape[0],
            list(genotype)
        )

    sql_insert_info = f"""
        INSERT INTO ga_run_info ({','.join(constants.cols_info)})
        VALUES %s;
        """

    execute_values(cursor, sql_insert_info, [data])

    conn.commit()


def start_one(init, estim, sel_type, l, n, px, use_mutation, runs, save_pair, sigma, const_1, const_2, sel_param1,
              sel_param2,
              maxN, random_state, title, stop_confluence):
    with open_db_cursor(constants.conn_str) as (cursor, conn):
        ids = []

        for i in range(runs):
            ids.append(
                store_settings(cursor, conn, i, init, estim, sel_type, l, n, px, use_mutation, sigma, const_1, const_2,
                               sel_param1, sel_param2, title))

        t = Thread(target=one_run, args=(
            init, estim, sel_type, l, n, px, use_mutation, ids, save_pair, sigma, const_1, const_2, sel_param1,
            sel_param2,
            maxN, random_state, stop_confluence))
        t.start()

        return ids


def one_run(init, estim, sel_type, l, n, px, use_mutation, ids, save_pair, sigma, const_1, const_2, sel_param1,
            sel_param2,
            maxN, random_state, stop_confluence):
    with open_db_cursor(constants.conn_str) as (cursor, conn):
        initialization = constants.INIT_MAP[init]
        pop = initialization(n, l, random_state=random_state)
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
                pop,
                sel_type,
                use_mutation,
                save_pair,
                sigma, const_1, const_2, sel_param1, sel_param2, maxN, stop_confluence
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
        cursor.execute(
            f"SELECT created_date, estim, s.id, sel_type, init, s.size_pop_type, run_id, l, s.n as n, title, max(i.iteration) as iters FROM ga_run_info i"
            f" inner join ga_run_settings s on s.id = i.ga_run_settings_id group by created_date, estim, s.id, sel_type, init, s.size_pop_type, run_id, l order by created_date desc")

        rows = [x for x in cursor]
        cols = [x[0] for x in cursor.description]

        runs = []
        for row in rows:
            run = {}
            for prop, val in zip(cols, row):
                if prop == 'chart':
                    continue
                if prop == 'created_date':
                    run[prop] = val
                if isinstance(val, str):
                    val = val.strip()
                run[prop] = val
            runs.append(run)

        runs_json = json.dumps(runs, cls=DjangoJSONEncoder)

        return runs_json


def get_chart(run_id):
    with open_db_cursor(constants.conn_str) as (cursor, conn):
        cursor.execute(f"SELECT chart FROM ga_run_settings "
                       f"where id = '{run_id}'")

        res = {'data': cursor.fetchone()[0].tobytes().decode("utf-8")}
        return json.dumps(res)


def get_info(run_id):
    with open_db_cursor(constants.conn_str) as (cursor, conn):
        cursor.execute(
            f"SELECT *, gi.id as id FROM ga_run_info gi INNER JOIN ga_run_settings gs on gi.ga_run_settings_id=gs.id "
            f"where ga_run_settings_id = '{run_id}' order by iteration asc")

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


def get_info_details(run_id):
    with open_db_cursor(constants.conn_str) as (cursor, conn):
        cursor.execute(f"SELECT health FROM ga_run_info "
                       f"where ga_run_settings_id = '{run_id}' and (iteration=0 or iteration=1)")

        rows = cursor.fetchall()
        health_before = np.array(rows[0][0])
        health_after = np.array(rows[1][0])
        m_before = health_before.mean()
        d_before = health_before.var()
        std_before = health_before.std()
        cv_before = variation(health_before, axis=0)
        r_before = health_before.max() - health_before.min()

        m_after = health_after.mean()
        d_after = health_after.var()
        std_after = health_after.std()
        cv_after = variation(health_after, axis=0)
        r_after = health_after.max() - health_after.min()

        res = {
            'm_before': float(m_before),
            'd_before': float(d_before),
            'std_before': float(std_before),
            'cv_before': float(cv_before),
            'r_before': float(r_before),
            'm_after': float(m_after),
            'd_after': float(d_after),
            'std_after': float(std_after),
            'cv_after': float(cv_after),
            'r_after': float(r_after),
        }
        return json.dumps(res)
