import matplotlib.pyplot as plt
import pandas.io.sql as sqlio

from old.database import open_db_cursor

with open_db_cursor('postgresql://misha:thesis_misha@146.148.7.100:5432/thesis') as (cur, conn):
    sql = f"""
        SELECT L, N, test_px
        FROM task1_aggr_gcloud_test_visualize2
        WHERE L>=20 AND L <= 150
        ORDER BY L, N
        """

    df = sqlio.read_sql_query(sql, conn)
    data = df.to_numpy()

    ax = plt.axes(projection='3d')
    ax.set_xlabel('L')
    ax.set_ylabel('N')
    ax.plot_trisurf(data[:, 0], data[:, 1], data[:, 2],
                    cmap='viridis', edgecolor='none')
    plt.show()
