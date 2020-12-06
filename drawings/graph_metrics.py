import numpy as np
import matplotlib.pyplot as plt
import pandas.io.sql as sqlio
from old.database import open_db_cursor


def get_data(conn_str, l, n, sel_type, init, run_id=0):
    with open_db_cursor(conn_str) as (cur, conn):
        sql = f"""
        SELECT run_id, expected_value_pair, expected_value_wild, expected_value_ideal,
                        std_pair, std_wild, std_ideal,
                        variance_coef_pair, variance_coef_wild, variance_coef_ideal,
    
                        mean_health, mean_health_diff_0, best_health_diff_0
        FROM task2_full_gcloud_v1
        WHERE L={l} AND N={n} AND sel_type='{sel_type}' AND init='{init}' AND run_id={run_id}
        ORDER BY run_id, iteration
        LIMIT 20000
        """

        df = sqlio.read_sql_query(sql, conn)
        data = df.to_numpy()

        return data


def plot():
    conn_str = "postgresql://misha:thesis_misha@146.148.7.100:5432/thesis"

    data1 = get_data(conn_str, 100, 100, 'rws', 'normal')
    data2 = get_data(conn_str, 100, 100, 'tournament_12', 'normal')

    ratio = 50

    fig = plt.figure()
    fig.set_size_inches(18.5, 8.5)
    fig.set_tight_layout(True)

    e_data1 = data1[data1[:, 0] == 0][:, 4]
    sm_e_data = e_data1.reshape(len(e_data1) // ratio, ratio).sum(axis=1) / ratio
    plt.plot(np.arange(0, len(sm_e_data)) * ratio, sm_e_data, color='g')

    e_data2 = data2[data2[:, 0] == 0][:, 4]
    sm_e_data2 = e_data2.reshape(len(e_data2) // ratio, ratio).sum(axis=1) / ratio
    plt.plot(np.arange(0, len(sm_e_data2)) * ratio, sm_e_data2, color='b')

    plt.show()


plot()
