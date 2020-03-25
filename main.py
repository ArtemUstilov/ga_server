from database import open_db_cursor
from tasks_static.task1_mean_h import try_px
from tasks_static.task_2 import start
from utils import get_pxs

GCLOUD_CONN_STR = ''
CONN_STR = ''


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


def run_static_task1_try_px():
    with open_db_cursor(CONN_STR) as (cursor, conn):
        try_px('task1_aggr_v6', 10, 200, 'rws', 0.00025269165039062497 * 2, cursor, conn)
