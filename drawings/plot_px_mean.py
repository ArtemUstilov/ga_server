import matplotlib.pyplot as plt
import pandas.io.sql as sqlio

from old.database import open_db_cursor

with open_db_cursor('postgresql://misha:thesis_misha@146.148.7.100:5432/thesis') as (cur, conn):
    sql = f"""
        SELECT unnest(t1.mean_health)
        FROM task1_extended_run_details_test t1 
        WHERE t1.run_id=420 AND t1.run_number=2
        LIMIT 20000;
        """

    df = sqlio.read_sql_query(sql, conn)
    data = df.to_numpy()
    plt.plot(data)

    plt.show()
