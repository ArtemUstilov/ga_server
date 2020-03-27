import numpy as np
from psycopg2.extras import execute_values

from core.mutation import mutate
from core import selection, estimation, initialization
from utils import simple_polymorphous, locus_roles_polymorphous

EPS = 0.0001
N_IT = 20000

INIT_MAP = {
    'all_0': initialization.all_zeros,
    'uniform': initialization.uniform,
    'normal': initialization.normal,
    'normal_with_locuses': initialization.normal_with_locuses,
}

ESTIMATION_MAP = {
    'all_l': estimation.const,
    'l-hamming_d': estimation.inverted_hamming_distance,
    'on_split_locuses': estimation.on_split_locuses,
    'sigma_2': estimation.sigma_2,
    'sigma_4': estimation.sigma_4,
    'sigma_10': estimation.sigma_10,
}

SELECTION_MAP = {
    'rws': selection.roulette,
    'tournament_2': selection.tournament_2,
    'tournament_4': selection.tournament_4,
    'tournament_12': selection.tournament_12,
}


def find_px_extended(table_name, inits, estims, sels, ls, ns, progons, cursor, conn):
    sql_insert = f"""
        INSERT INTO {table_name} ({','.join(cols_aggr)})
        VALUES %s
        RETURNING id;
    """
    sql_insert2 = f"""
        INSERT INTO {table_name}_run_details ({','.join(cols_details)})
        VALUES %s
        RETURNING id;
    """
    for init in inits:
        init_func = INIT_MAP[init]
        for estim in estims:
            estimation_func = ESTIMATION_MAP[estim]
            for sel in sels:
                selection_func = SELECTION_MAP[sel]
                for l in ls:
                    for n in ns:
                        px = 1 / (50 * l)
                        print((init, estim, sel, l, n, px), ': ', end='')
                        sigma = px * 0.5
                        for i in range(15):
                            print(i, end=' ')
                            count_successful = 0
                            run_results = []
                            run_mean_h = []
                            run_poly_p1 = []
                            run_poly_p2 = []

                            for j in range(progons):
                                fin_iter_num, mean_h, poly_p1, poly_p2 = run_aggr(init_func,
                                                                                  estimation_func,
                                                                                  selection_func,
                                                                                  l, n, px,
                                                                                  cursor
                                                                                  )
                                run_results.append(fin_iter_num)
                                run_mean_h.append(mean_h)
                                run_poly_p1.append(poly_p1)
                                run_poly_p2.append(poly_p2)
                                if fin_iter_num + 1 < N_IT:
                                    count_successful += 1
                                else:
                                    break

                            store_in_db_aggr(
                                cursor=cursor,
                                conn=conn,
                                sql_script=sql_insert,
                                sql_insert2=sql_insert2,
                                l=l,
                                n=n,
                                init=init,
                                estim=estim,
                                sel_type=sel,
                                try_id=i,
                                cur_px=px,
                                runs_results=run_results,
                                run_mean_h=run_mean_h,
                                poly_p1=run_poly_p1,
                                poly_p2=run_poly_p2,
                                count_succ=count_successful,
                                is_final=i == 14
                            )

                            if count_successful == progons:
                                px += sigma
                            else:
                                px -= sigma

                            sigma = sigma * 0.5
                        print('!')


def test_px_extended(table_from_name,
                     table_to_name,
                     table_details_name,
                     progons, cursor, conn, rows=None, add_select=''):
    sql_select = f"""
        SELECT id, init, estim, type, l, n, cur_px
        FROM {table_from_name}
        WHERE chosen_for_test=true AND id NOT IN (SELECT record_id FROM {table_to_name} 
                                                    WHERE  record_id IS NOT NULL)
            {add_select}
        ORDER BY type;
    """

    sql_insert_test = f"""
    INSERT INTO {table_to_name} ({','.join(cols_aggr_test)})
    VALUES %s
    RETURNING id;
    """

    sql_insert2 = f"""
        INSERT INTO {table_details_name} ({','.join(cols_details_percent)})
        VALUES %s;
        """

    if not rows:
        cursor.execute(sql_select)
        rows = cursor.fetchall()

    for (rec_id, init, estim, sel_type, l, n, cur_px) in rows:
        print((rec_id, init, estim, sel_type, l, n, cur_px))
        init_func = INIT_MAP[init]
        estimation_func = ESTIMATION_MAP[estim]
        selection_func = SELECTION_MAP[sel_type]

        # Testing px
        count_successful = 0
        run_results = []
        mean_h_ar = []
        poly_p1s = []
        poly_p2s = []
        for j in range(progons):
            successful, mean_health, poly_p1, poly_p2 = run_aggr(init_func,
                                                                 estimation_func,
                                                                 selection_func,
                                                                 l, n, cur_px,
                                                                 cursor)
            run_results.append(successful)
            mean_h_ar.append(mean_health)
            poly_p1s.append(poly_p1)
            poly_p2s.append(poly_p2)
            if successful + 1 < N_IT:
                count_successful += 1
        print('1:', run_results)

        # Testing 1.2*px
        px120 = 1.2 * cur_px
        count_successful120 = 0
        mean_h_ar120 = []
        poly_p1s120 = []
        poly_p2s120 = []
        run_results120 = []
        for j in range(progons):
            successful, mean_health, poly_p1, poly_p2 = run_aggr(init_func,
                                                                 estimation_func,
                                                                 selection_func,
                                                                 l, n, px120,
                                                                 cursor)
            run_results120.append(successful)
            mean_h_ar120.append(mean_health)
            poly_p1s120.append(poly_p1)
            poly_p2s120.append(poly_p2)
            if successful + 1 < N_IT:
                count_successful120 += 1

        print('2:', run_results120)
        # Testing 0.8*px
        px80 = 0.8 * cur_px
        count_successful80 = 0
        run_results80 = []
        mean_h_ar80 = []
        poly_p1s80 = []
        poly_p2s80 = []
        run_results120 = []
        for j in range(progons):
            successful, mean_health, poly_p1, poly_p2 = run_aggr(init_func,
                                                                 estimation_func,
                                                                 selection_func,
                                                                 l, n, px80,
                                                                 cursor)
            run_results80.append(successful)
            mean_h_ar80.append(mean_health)
            poly_p1s80.append(poly_p1)
            poly_p2s80.append(poly_p2)
            if successful + 1 < N_IT:
                count_successful80 += 1
        print('3:', run_results80)

        data = (
            rec_id,
            l,
            n,
            init,
            estim,
            sel_type,
            cur_px,
            run_results,
            count_successful,
            px120,
            run_results120,
            count_successful120,
            px80,
            run_results80,
            count_successful80,
        )

        execute_values(cursor, sql_insert_test, [data])
        conn.commit()
        res = cursor.fetchall()

        data2 = [(
            res[0][0],
            i,
            100,
            mean_h_ar[i],
            poly_p1s[i],
            poly_p2s[i]
        ) for i in range(len(run_results))]
        execute_values(cursor, sql_insert2, data2)

        data2 = [(
            res[0][0],
            i,
            120,
            mean_h_ar120[i],
            poly_p1s120[i],
            poly_p2s120[i]
        ) for i in range(len(run_results))]
        execute_values(cursor, sql_insert2, data2)

        data2 = [(
            res[0][0],
            i,
            80,
            mean_h_ar80[i],
            poly_p1s80[i],
            poly_p2s80[i]
        ) for i in range(len(run_results))]
        execute_values(cursor, sql_insert2, data2)


def run_aggr(init_func, estimation_func, selection_func, l, n, px, cursor):
    kwargs = {}
    if 'locuses' in estimation_func.__name__ or 'locuses' in selection_func.__name__:
        cursor.execute(
            f"SELECT good_locuses, bad_locuses, lethal_locuses  FROM locus_helper WHERE l={l}")
        row = cursor.fetchone()

        kwargs.update({
            'good': np.array(row[0], dtype=np.int8),
            'bad': np.array(row[1], dtype=np.int8),
            'lethal': np.array(row[2], dtype=np.int8)
        })

    pop = init_func(l, n, **kwargs)
    health = estimation_func(pop, **kwargs)

    # Start loop
    last_mean_health = health.mean()
    final_iter_num = N_IT - 1
    last_counter = 0
    poly_d1 = []
    poly_d2 = []
    mean_health_ar = []

    for i in range(0, N_IT):
        pop = selection_func(pop, health, n, **kwargs)
        pop = mutate(pop, px)
        health = estimation_func(pop)
        mean_health = health.mean()
        mean_health_ar.append(mean_health)

        if abs(last_mean_health - mean_health) < EPS:
            last_counter += 1
        else:
            last_counter = 0
        if last_counter >= 10:
            final_iter_num = i
            break
        last_mean_health = mean_health
        if 'good' in kwargs:
            poly_d1.append(locus_roles_polymorphous(pop, **kwargs))
            poly_d2.append(locus_roles_polymorphous(pop, v=1, **kwargs))
        else:
            poly_d1.append(simple_polymorphous(pop))
            poly_d2.append(simple_polymorphous(pop, v=1))

    return final_iter_num, mean_health_ar, poly_d1, poly_d2


cols_aggr = [
    'L',
    'N',
    'init',
    'estim',
    'type',
    'try_id',
    'cur_px',
    'runs_succ',
    'count_succ',
    'is_final',
    'chosen_for_test',
]

cols_aggr_test = [
    'record_id',
    'L',
    'N',
    'init',
    'estim',
    'type',
    'test_px',
    'runs_succ',
    'count_succ',
    'test_px120',
    'runs_succ120',
    'count_succ120',
    'test_px80',
    'runs_succ80',
    'count_succ80',
]

cols_details = [
    'run_id',
    'run_number',
    'mean_health',
    'polymorphous1_p',
    'polymorphous2_p'
]

cols_details_percent = [
    'run_id',
    'run_number',
    'percent',
    'mean_health',
    'polymorphous1_p',
    'polymorphous2_p'
]


def store_in_db_aggr(cursor, conn, sql_script, sql_insert2, l, n, init, estim, sel_type,
                     try_id, cur_px, runs_results, run_mean_h, poly_p1, poly_p2,
                     count_succ, is_final):
    print('')
    data = (
        l,
        n,
        init,
        estim,
        sel_type,
        try_id,
        cur_px,
        runs_results,
        count_succ,
        is_final,
        False,
    )

    execute_values(cursor, sql_script, [data])
    conn.commit()
    result = cursor.fetchall()

    data2 = [(
        result[0][0],
        i,
        run_mean_h[i],
        poly_p1[i],
        poly_p2[i],
    ) for i in range(len(runs_results))]
    execute_values(cursor, sql_insert2, data2)
    conn.commit()
