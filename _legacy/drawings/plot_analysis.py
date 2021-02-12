import matplotlib.pyplot as plt
import numpy as np
import pandas.io.sql as sqlio
import base64
import io
from psycopg2.extras import execute_values

from server.thesis.core.database import open_db_cursor


def get_first(el):
    return el[0]


def get_index_when_grow_stops(n):
    ll = len(n)
    for i in range(1, ll):
        if n[ll-i] != n[ll-1-i]:
            return ll-i
    return 0

with open_db_cursor('postgresql://postgres:123123Aa@146.148.7.100:5432/thesis') as (cur, conn):
    sql = f"""
        SELECT DISTINCT run_id, sel_type, size_pop_type, l, estim, init
        FROM task_2_variant_2
        """

    df = sqlio.read_sql_query(sql, conn)
    runs = df.to_numpy()

    for i in range(len(runs)):
        # if i > 0:
        #     break
        row = runs[i]

        ttype = (str(row[2])).strip()
        init = row[5].strip()
        run_id = row[0]
        l = row[3]
        estim = row[4].strip()
        sel_type = row[1].strip()


        sql = f"""
            SELECT iteration, min_pair, max_pair, min_wild, max_wild, min_ideal, 
            max_ideal, mode_pair, mode_ideal, mode_wild, std_pair, std_wild, std_ideal,
            n, expected_value_pair, expected_value_ideal,expected_value_wild
            FROM task_2_variant_2
            WHERE l = {l} AND size_pop_type = '{ttype}' AND sel_type = '{sel_type}' AND init = '{init}' AND run_id = {run_id} AND estim='{estim}'
            ORDER BY iteration
            """

        df = sqlio.read_sql_query(sql, conn)
        data = df.to_numpy()

        fig = plt.figure(figsize=(20,16))

        ind_stop = get_index_when_grow_stops(data[:,13])

        iteration = data[:, 0]
        min_pair = data[:, 1]
        max_pair = data[:, 2]
        expected_pair = np.array(data[:, 14]*max_pair.max()/2, dtype=float)
        std_pair = np.array(data[:, 10]*max_pair.max()/2, dtype=float)
        mode_pair = np.vectorize(get_first)(data[:, 7])*max_pair.max()/2

        min_wild = data[:, 3]
        max_wild = data[:, 4]
        expected_wild = np.array(data[:, 16]*max_wild.max()/2, dtype=float)
        std_wild = np.array(data[:, 11]*max_wild.max()/2, dtype=float)
        mode_wild = np.vectorize(get_first)(data[:, 9])*max_wild.max()/2

        min_ideal = data[:, 5]
        max_ideal = data[:, 6]
        expected_ideal = np.array(data[:, 15] * max_ideal.max() / 2, dtype=float)
        std_ideal = np.array(data[:, 12] * max_ideal.max() / 2, dtype=float)
        mode_ideal = np.vectorize(get_first)(data[:, 8]) * max_ideal.max() / 2

        ax = fig.add_subplot(3, 1, 1)

        ax.axvline(ind_stop, color='blue')
        ax.text(ind_stop + 0.1, max_pair.max()/2, "stop growing on {} iteration".format(ind_stop), rotation=90)
        ax.set_title('Pair')
        ax.plot(iteration, min_pair, color='brown', label='min_pair')
        ax.plot(iteration, max_pair, color='green', label='max_pair')
        ax.plot(iteration, expected_pair, color='purple', label='expected_pair', linewidth=0.5)
        ax.plot(iteration, mode_pair, color='orange', label='mode_pair',  linewidth=0.5)
        ax.fill_between(np.array(iteration, dtype=int), std_pair, expected_pair, color='blue', alpha=0.5)
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=3)

        ax2 = fig.add_subplot(3, 1, 2)
        ax2.axvline(ind_stop, color='blue')
        ax2.text(ind_stop + 0.1, max_wild.max()/2, "stop growing on {} iteration".format(ind_stop), rotation=90)
        ax2.set_title('Wild')
        ax2.plot(iteration, min_wild, color='brown', label='min_wild')
        ax2.plot(iteration, max_wild, color='green', label='max_wild')
        ax2.plot(iteration, expected_wild, color='purple', label='expected_wild')
        ax2.plot(iteration, mode_wild, color='orange', label='mode_wild')
        ax2.fill_between(np.array(iteration, dtype=int), std_wild, expected_wild, color='blue', alpha=0.5)

        ax3 = fig.add_subplot(3, 1, 3)
        ax3.axvline(ind_stop, color='blue')
        ax3.text(ind_stop + 0.1, max_ideal.max()/2, "stop growing on {} iteration".format(ind_stop), rotation=90)
        ax3.set_title('Ideal')
        ax3.plot(iteration, min_ideal, color='brown', label='min_ideal')
        ax3.plot(iteration, max_ideal, color='green', label='max_ideal')
        ax3.plot(iteration, expected_ideal, color='purple', label='expected_ideal')
        ax3.plot(iteration, mode_ideal, color='orange', label='mode_ideal')
        ax3.fill_between(np.array(iteration, dtype=int), std_ideal, expected_ideal, color='blue', alpha=0.5)

        pic_IObytes = io.BytesIO()
        fig.savefig(pic_IObytes, format='png', bbox_inches='tight')
        pic_IObytes.seek(0)
        pic_hash = base64.b64encode(pic_IObytes.read()).decode('utf8')
        sql = f"""
           
           
                INSERT INTO charts (chart_name, data)
                VALUES %s
                ON CONFLICT (chart_name) DO UPDATE 
                    SET data = excluded.data;
                """
        # fig.show()
        execute_values(cur, sql, [(
                    '{}__l-{}__estim-{}__init-{}__select-{}__v-1__runid-{}.png'.format(ttype, l, estim, init, sel_type, run_id),
                    pic_hash
                )])
        conn.commit()

        # fig.savefig('{}__l-{}__estim-{}__init-{}__select-{}__v-1__runid-{}.png'.format(ttype, l, run_id, estim, init, sel_type))
