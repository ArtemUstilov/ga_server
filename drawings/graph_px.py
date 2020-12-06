import numpy as np
import matplotlib.pyplot as plt

from old.database import open_db_cursor

with open_db_cursor('bla') as (cursor, conn):
    sql = """
    SELECT l, final_px
    FROM final_pxs
    WHERE N=100
    ORDER BY L;
    """
    cursor.execute(sql)
    rows = cursor.fetchall()

    data_x = np.array([row[0] for row in rows])
    data_y = np.array([row[1] for row in rows])
    plt.plot(data_x, data_y)
    plt.show()
