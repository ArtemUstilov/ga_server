import matplotlib.pyplot as plt
import numpy as np
import pandas.io.sql as sqlio

from database import open_db_cursor

with open_db_cursor('postgresql://thesis:thesis@localhost:5432/thesis') as (cur, conn):
    sql = f"""
        SELECT run_mean_h
        FROM task1_aggr_v6
        WHERE id=19
        """
    cur.execute(sql)
    row = cur.fetchone()

    plt.plot(row[0][:1000], c='b')

    plt.show()
