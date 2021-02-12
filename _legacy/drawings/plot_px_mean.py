import matplotlib.pyplot as plt
import pandas.io.sql as sqlio

from server.thesis.core.database import open_db_cursor

with open_db_cursor('') as (cur, conn):
    sql = f"""
        SELECT test_px120, (select avg(a) from unnest(runs_succ) as a) as r
        FROM task1_visualize_mean
        WHERE id > 93
        ORDER BY test_px120
        """

    df = sqlio.read_sql_query(sql, conn)
    data = df.to_numpy()
    plt.plot(data[:, 0], data[:, 1])

    plt.show()
