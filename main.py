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
