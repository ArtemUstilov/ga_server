import matplotlib.pyplot as plt
import numpy as np
import pandas.io.sql as sqlio

from database import open_db_cursor

with open_db_cursor('postgresql://thesis:thesis@localhost:5432/thesis_bump') as (cur, conn):

    for N, c in zip([100, 120, 140, 160, 180, 195],
                    ['tab:blue','tab:orange','tab:green','tab:red','tab:purple','tab:olive','tab:brown', 'tab:pink']):
        sql = f"""
        SELECT l, test_px
        FROM task1_aggr_gcloud_test_visualize
        WHERE N = {N}
        ORDER BY l
        """

        df = sqlio.read_sql_query(sql, conn)
        data = df.to_numpy()

        ham, = plt.plot(data[:,0], data[:,1], c=c, label=f'N={N}')
    plt.legend()
    plt.xlabel("L")
    plt.ylabel("Pmax")
    plt.title('RWS')
    plt.show()
