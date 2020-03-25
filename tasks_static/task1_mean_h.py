import numpy as np
from psycopg2.extras import execute_values

from core import selection
from core.estimation import hamming_distance
from core.initialization import uniform
from core.mutation import mutate
from core.selection import roulette

EPS = 0.0001
N_IT = 20000


def run_aggr(l, n, px, selection_func):
    # Initialization
    pop = uniform(n, l)
    health = l - hamming_distance(pop)

    # Start loop
    last_mean_health = health.mean()
    final_iter_num = N_IT - 1
    last_counter = 0
    mean_health_ar = np.zeros(N_IT)

    for i in range(0, N_IT):
        pop = selection_func(pop, health, n)
        pop = mutate(pop, px)
        health = l - hamming_distance(pop)
        mean_health = health.mean()
        mean_health_ar[i] = mean_health

        if abs(last_mean_health - mean_health) < EPS:
            last_counter += 1
        else:
            last_counter = 0
        if last_counter >= 10:
            final_iter_num = i
            break
        last_mean_health = mean_health

    return final_iter_num, mean_health_ar


def store_in_db_aggr(cursor, conn, sql_script, l, n, sel_type,
                     try_id, cur_px, runs_results, run_mean_h):
    data = (
        l,
        n,
        sel_type,
        try_id,
        cur_px,
        runs_results,
        run_mean_h,
        None,
        None,
        False,
        False
    )

    execute_values(cursor, sql_script, [data])
    conn.commit()


cols_aggr = [
    'L',
    'N',
    'type',
    'try_id',
    'cur_px',
    'runs_succ',
    'run_mean_h',
    'count_succ',
    'is_final',
    'chosen_for_test',
    'is_result',
]


def rws(pop, health, n_ind):
    return roulette(pop, health, n_ind)


def tournament_2(pop, health, n_ind):
    return selection.tournament_2(pop, health, n_ind)


def tournament_4(pop, health, n_ind):
    return selection.tournament_4(pop, health, n_ind)


def tournament_12(pop, health, n_ind):
    return selection.tournament_12(pop, health, n_ind)


SELECTION_MAP = {
    'rws': rws,
    'tournament_2': tournament_2,
    'tournament_4': tournament_4,
    'tournament_12': tournament_12,
}


def try_px(table_name, l, n, sel, px, cursor, conn):
    sql_insert = f"""
    INSERT INTO {table_name} ({','.join(cols_aggr)})
    VALUES %s;
    """

    selection_func = SELECTION_MAP[sel]
    print((l, n, sel, px))

    fin_iter_num, mean_healths = run_aggr(l, n, px, selection_func)

    store_in_db_aggr(
        cursor=cursor,
        conn=conn,
        sql_script=sql_insert,
        l=l,
        n=n,
        sel_type=selection_func.__name__,
        try_id=1,
        cur_px=px,
        runs_results=[fin_iter_num],
        run_mean_h=list(mean_healths[:fin_iter_num+1]),
    )
