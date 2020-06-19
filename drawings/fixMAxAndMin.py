import matplotlib.pyplot as plt
import numpy as np
import pandas.io.sql as sqlio
import base64
import io
from psycopg2.extras import execute_values
from matplotlib.pyplot import text

from database import open_db_cursor


with open_db_cursor('postgresql://postgres:123123Aa@146.148.7.100:5432/thesis') as (cur, conn):
    sql = f"""
        SELECT id, pairwise_hamming_distribution_p, ideal_hamming_distribution_p,
            wild_type_hamming_distribution_p
        FROM task_2_variant_2
        """

    df = sqlio.read_sql_query(sql, conn)
    runs = df.to_numpy()
    # print(runs)
    max_pair = []
    min_pair = []
    max_ideal = []
    min_ideal = []
    max_wild = []
    min_wild = []
    for i in range(len(runs)):
        max_pair.append(int(np.array(runs[i][1]).argmax()))
        min_pair.append(int(np.array(runs[i][1]).argmin()))
        max_ideal.append(int(np.array(runs[i][2]).argmax()))
        min_ideal.append(int(np.array(runs[i][2]).argmin()))
        max_wild.append(int(np.array(runs[i][3]).argmax()))
        min_wild.append(int(np.array(runs[i][3]).argmin()))
    print(list(runs[:,0].astype(int)) )
    data = np.array([list(runs[:,0].astype(int)), list(max_pair), list(min_pair),
                               list(max_ideal), list(min_ideal), list(max_wild), list(min_wild)]).transpose()
    print(data)
    sql = f"""
          UPDATE task_2_variant_2 AS t SET 
                max_pair=e.max_pair, 
                min_pair=e.min_pair, 
                max_wild=e.max_wild, 
                min_wild=e.min_wild, 
                max_ideal=e.max_ideal, 
                min_ideal=e.min_ideal
          FROM (VALUES %s) AS e(id, max_pair, min_pair, max_ideal, min_ideal, max_wild, min_wild) 
          WHERE t.id = CAST ( e.id AS integer )
          """
    execute_values(cur, sql, data.tolist())