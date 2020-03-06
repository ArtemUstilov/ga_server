import matplotlib.pyplot as plt
import numpy as np
import pandas.io.sql as sqlio

from database import open_db_cursor

with open_db_cursor('') as (cur, conn):
    sql = f"""
        SELECT L, test_px
        FROM task1_aggr_gcloud_test_visualize
        WHERE N = 195
        ORDER BY L, N
        """

    df = sqlio.read_sql_query(sql, conn)
    data = df.to_numpy()
    plt.plot(data[:, 0], data[:, 1])

    plt.show()
