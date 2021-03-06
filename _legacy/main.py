from server.thesis.core.database import open_db_cursor
from server.thesis.core.utils import write_locuses_roles

if __name__ == '__main__':
    conn_str = "dbname=%s host=%s port=%d user=%s password=%s" % \
               ("thesis", "localhost", 5432, "artemustilov", "")

    with open_db_cursor(conn_str) as (cursor, conn):
        write_locuses_roles(cursor, conn, [10, 20, 100, 1000, 2000])
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