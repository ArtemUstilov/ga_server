from database import open_db_cursor
from tasks_static.task1_extended import find_px_extended, test_px_extended
from tasks_static.task_2 import start
from utils import get_pxs



def run_static_task2():
    pxs = get_pxs(CONN_STR, 0.9)
    start(CONN_STR, 'task2_full_gcloud_v1',
          ['normal'],
          ['on_split_locuses'],
          [100],
          [100],
          ['tournament_2'],
          pxs,
          [1, 2, 3, 4]
          )


def run_static_task1_find_px_extended():
    with open_db_cursor(GCLOUD_CONN_STR) as (cursor, conn):
        find_px_extended('task1_extended', ['uniform'],
                         ['l-hamming_d'],
                         ['tournament_4'], [10], [100], 10, cursor, conn)


def run_static_task1_test_px_extended():
    with open_db_cursor(GCLOUD_CONN_STR) as (cursor, conn):
        test_px_extended(
            'task1_extended', 'task1_extended_test', 'task1_extended_run_details_test',
            10, cursor, conn, add_select=' AND id=115'
        )


def run_static_task1_retest_px_extended():
    with open_db_cursor(GCLOUD_CONN_STR) as (cursor, conn):
        sql = """
        SELECT init, estim, type, l, n, test_px * 0.9
        FROM task1_extended_test_3
        WHERE count_succ <> 10 AND estim='l-hamming_d' AND type='rws'
        ORDER BY init, estim, type, l, n;
        """
        cursor.execute(sql)
        rows = cursor.fetchall()
        rows = [
            (None, row[0], row[1], row[2], row[3], row[4], row[5])
            for row in rows
        ]
        test_px_extended(
            '', 'task1_extended_test', 'task1_extended_run_details_test',
            10, cursor, conn, rows=rows
        )


if __name__ == '__main__':
    run_static_task1_test_px_extended()


from task_dynamic.task_2_variant2 import start, INIT_MAP, ESTIM_MAP, SELECTION_MAP
from core.initialization import normal

if __name__ == '__main__':
    conn_str = "dbname=%s host=%s port=%d user=%s password=%s" % \
               ("thesis", "146.148.7.100", 5432, "postgres", "123123Aa")
    print(normal(10,5))
    # start(
    #     conn_str,
    #     "task_2_variant_2",
    #     ['normal'],
    #     ['on_split_locuses'],
    #     [200],
    #     ['rws'],
    #     {
    #         (10, 1000, 'rws'): 5.43884e-05 * 0.9,
    #         (20, 1000, 'rws'): 2.37305e-05 * 0.9,
    #         (80, 1000, 'rws'): 4.3808e-06 * 0.9,
    #         (200, 1000, 'rws'): 1.62598e-06 * 0.9,
    #         (10, 2000, 'rws'): 2.72217e-05 * 0.9,
    #         (20, 2000, 'rws'): 1.26343e-05 * 0.9,
    #         (80, 2000, 'rws'): 2.54822e-06 * 0.9,
    #         (200, 2000, 'rws'): 7.69043e-07 * 0.9,
    #         (10, 1000, 'tournament_2'): 5.43884e-05 * 0.9,
    #         (20, 1000, 'tournament_2'): 2.37305e-05 * 0.9,
    #         (80, 1000, 'tournament_2'): 4.3808e-06 * 0.9,
    #         (200, 1000, 'tournament_2'): 1.62598e-06 * 0.9,
    #         (10, 2000, 'tournament_2'): 2.72217e-05 * 0.9,
    #         (20, 2000, 'tournament_2'): 1.26343e-05 * 0.9,
    #         (80, 2000, 'tournament_2'): 2.54822e-06 * 0.9,
    #         (200, 2000, 'tournament_2'): 7.69043e-07 * 0.9,
    #     },
    #     ['type_3_init_200'],
    #     1
    # )

