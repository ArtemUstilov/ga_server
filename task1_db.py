from psycopg2.extras import execute_values

from database import open_db_cursor
from estimation import hamming_distance
from initialization import uniform
from mutation import mutate
from selection import roulette, tournament

EPS = 0.0001
N_IT = 20000


def run_aggr(l, n, px, selection_func):
    # Initialization
    pop = uniform(n, l)
    health = l - hamming_distance(pop)

    # Start loop
    last_mean_health = health.mean()
    successful = False
    last_counter = 0

    for i in range(1, N_IT):
        pop = selection_func(pop, health, n)
        pop = mutate(pop, px)
        health = l - hamming_distance(pop)
        mean_health = health.mean()

        if abs(last_mean_health - mean_health) < EPS:
            last_counter += 1
        else:
            last_counter = 0
        if last_counter >= 10:
            successful = True
            break
        last_mean_health = mean_health

    return successful


def store_in_db_aggr(cursor, conn, sql_script, l, n, sel_type,
                     try_id, cur_px, runs_results, count_succ, is_final):
    data = (
        l,
        n,
        sel_type,
        try_id,
        cur_px,
        runs_results,
        count_succ,
        is_final,
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
    'count_succ',
    'is_final',
    'chosen_for_test',
    'is_result',
]

cols_aggr_test = [
    'record_id',
    'L',
    'N',
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


def rws(pop, health, n_ind):
    return roulette(pop, health, n_ind)


def tournament_2(pop, health, n_ind):
    return tournament(pop, health, n_ind, 2)


def tournament_4(pop, health, n_ind):
    return tournament(pop, health, n_ind, 4)


def tournament_12(pop, health, n_ind):
    return tournament(pop, health, n_ind, 12)


SELECTION_MAP = {
    'rws': rws,
    'tournament_2': tournament_2,
    'tournament_4': tournament_4,
    'tournament_12': tournament_12,
}


def find_px(table_name):
    sql_insert = f"""
    INSERT INTO {table_name} ({','.join(cols_aggr)})
    VALUES %s;
    """

    with open_db_cursor() as (cursor, conn):
        for selection_func in [rws, tournament_2, tournament_4, tournament_12]:
            print('Selection:', selection_func.__name__)
            for l in [10, 20, 80, 100, 200]:
                print('L:', l)
                for n in [100, 200]:
                    print('\tn:', n)
                    px = 1 / (50 * l)
                    sigma = px * 0.5
                    for i in range(15):
                        print('\t\ti:', i)
                        count_successful = 0
                        run_results = []
                        for j in range(10):
                            print('\t\t\tj:', j)
                            successful = run_aggr(l, n, px, selection_func)
                            run_results.append(successful)
                            if successful:
                                count_successful += 1
                            else:
                                break

                        store_in_db_aggr(
                            cursor=cursor,
                            conn=conn,
                            sql_script=sql_insert,
                            l=l,
                            n=n,
                            sel_type=selection_func.__name__,
                            try_id=i,
                            cur_px=px,
                            runs_results=run_results,
                            count_succ=count_successful,
                            is_final=i == 14
                        )

                        if count_successful == 10:
                            px += sigma
                        else:
                            px -= sigma

                        sigma = sigma * 0.5


def find_px_v2(table_name):
    sql_aggr = f"""
    INSERT INTO {table_name} ({','.join(cols_aggr)})
    VALUES %s;
    """

    with open_db_cursor() as (cursor, conn):
        for l in [20]:
            print('L:', l)
            for n in [100]:
                print('\tn:', n)
                left = 0
                right = 0.1
                for try_id in range(40):
                    print('\t\ttry_id:', try_id)
                    px = (left + right) * 0.5
                    count_succ = 0
                    run_results = []
                    for run_id in range(10):
                        print('\t\t\tRun_id:', run_id)
                        succ = run_aggr(l, n, px)
                        run_results.append(succ)
                        if succ:
                            count_succ += 1
                        else:
                            break

                    store_in_db_aggr(cursor, conn, sql_aggr, l, n,
                                     'rws', try_id, px, run_results, count_succ, try_id == 14)
                    if count_succ == 10:
                        left = px
                    else:
                        right = px


def test_px(table_from_name, table_to_name):
    sql_select = f"""
        SELECT id, type, l, n, cur_px 
        FROM {table_from_name}
        WHERE is_final=true
        ORDER BY type;
    """

    sql_insert_test = f"""
    INSERT INTO {table_to_name} ({','.join(cols_aggr_test)})
    VALUES %s;
    """

    with open_db_cursor() as (cursor, conn):
        cursor.execute(sql_select)
        rows = cursor.fetchall()
        for (rec_id, sel_type, l, n, cur_px) in rows:
            print((sel_type, l, n, cur_px))
            # Testing px
            count_successful = 0
            run_results = []
            for j in range(10):
                successful = run_aggr(l, n, cur_px, SELECTION_MAP[sel_type])
                run_results.append(successful)
                if successful:
                    count_successful += 1
            print('1:', run_results)
            # Testing 1.2*px
            px120 = 1.2 * cur_px
            count_successful120 = 0
            run_results120 = []
            for j in range(10):
                successful = run_aggr(l, n, px120, SELECTION_MAP[sel_type])
                run_results120.append(successful)
                if successful:
                    count_successful120 += 1
            print('2:', run_results120)

            # Testing 0.8*px
            px80 = 0.8 * cur_px
            count_successful80 = 0
            run_results80 = []
            for j in range(10):
                successful = run_aggr(l, n, px80, SELECTION_MAP[sel_type])
                run_results80.append(successful)
                if successful:
                    count_successful80 += 1
            print('3:', run_results80)

            data = (
                rec_id,
                l,
                n,
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
