import matplotlib.pyplot as plt
import pandas.io.sql as sqlio

from server.thesis.core.database import open_db_cursor

with open_db_cursor('postgresql://misha:thesis_misha@146.148.7.100:5432/thesis') as (cur, conn):
    sql = f"""
        SELECT L, test_px
        FROM task1_aggr_gcloud_test_visualize
        WHERE N = 195
        ORDER BY L, N
        """

    df = sqlio.read_sql_query(sql, conn)
    data = df.to_numpy()
    plt.plot(data[:, 0], data[:, 1], c='b')

    sql = f"""
            SELECT L, test_px
            FROM task1_aggr_gcloud_test_visualize2
            WHERE N = 195
            ORDER BY L, N
            """

    df = sqlio.read_sql_query(sql, conn)
    data = df.to_numpy()
    plt.plot(data[:, 0], data[:, 1], c='g')

    plt.show()
