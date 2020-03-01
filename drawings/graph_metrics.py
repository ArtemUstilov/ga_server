from time import sleep

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.widgets import Slider, Button, TextBox
import pandas.io.sql as sqlio
from database import open_db_cursor

with open_db_cursor('bal') as (cur, conn):
    sql = f"""
    SELECT run_id,
                        expected_value_pair, expected_value_wild, expected_value_ideal,
                        std_pair, std_wild, std_ideal,
                        variance_coef_pair, variance_coef_wild, variance_coef_ideal,

                        mean_health, mean_health_diff_0, best_health_diff_0
    FROM task2_full_v1
    WHERE L=100 AND N=200 AND sel_type='rws'
    ORDER BY run_id, iteration
    LIMIT 60000
    """
    ratio = 50
    df = sqlio.read_sql_query(sql, conn)
    data = df.to_numpy()
    fig = plt.figure()
    fig.set_size_inches(18.5, 8.5)
    fig.set_tight_layout(True)

    for i, c in [(0, 'g'), (1, 'b'), (2, 'r')]:
        e_data1 = data[data[:, 0] == i][:, 1]
        sm_e_data = e_data1.reshape(len(e_data1) // ratio, ratio).sum(axis=1) / ratio
        plt.plot(np.arange(0, 20000, ratio), sm_e_data, color=c)

    plt.show()

    # plt.plot(data[:, 2], color='r')
    # plt.show()
    # plt.plot(data[:, 3], color='g')
    # plt.show()
    # plt.plot(data[:, 4])
    # plt.show()
    # plt.plot(data[:, 7])
    # plt.show()
    # plt.plot(data[:, 10])
    # plt.show()
    # plt.plot(data[:, 11])
    # plt.show()
    # plt.plot(data[:, 12])
    # plt.show()
