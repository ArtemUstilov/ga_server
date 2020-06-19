import matplotlib.pyplot as plt
import numpy as np
import pandas.io.sql as sqlio

from database import open_db_cursor

with open_db_cursor('') as (cur, conn):
    sql = f"""
        SELECT test_px120, (select MAX(a) from unnest(runs_succ) as a) as avg
        FROM task1_visualize_mean
        WHERE id>=94
        """
    cur.execute(sql)
    row = np.array(cur.fetchall())

    plt.plot(row[:, 0], row[:, 1], c='b')
    plt.plot([-40, 40], [20000, 20000], '--', c='r')
    plt.xlabel('%')
    plt.ylabel('Iteration')
    plt.show()
