import matplotlib.pyplot as plt
import pandas.io.sql as sqlio

from old.database import open_db_cursor

def main():
    with open_db_cursor('postgresql://thesis:thesis@localhost:5432/thesis_bump') as (cur, conn):
        def compare_estims():
            sql = f"""
            SELECT l * n, AVG(final_px)
            FROM final_pxs_extended
            WHERE estim='sigma_2' AND type='tournament_2' AND
                  L IN (10, 20, 80, 100, 200) AND N IN (100, 200) GROUP BY l*n
            ORDER BY l * n
            """

            df = sqlio.read_sql_query(sql, conn)
            data = df.to_numpy()

            s2, = plt.plot(data[:,0], data[:,1], c='blue', label='sigma_2')

            sql = f"""
                        SELECT l * n, AVG(final_px)
                        FROM final_pxs_extended
                        WHERE estim='sigma_4' AND type='tournament_2' AND
                              L IN (10, 20, 80, 100, 200) AND N IN (100, 200) GROUP BY l*n
                        ORDER BY l * n
                        """

            df = sqlio.read_sql_query(sql, conn)
            data = df.to_numpy()

            s4, = plt.plot(data[:, 0], data[:, 1], c='green', label='sigma_4')

            sql = f"""
                        SELECT l * n, AVG(final_px)
                        FROM final_pxs_extended
                        WHERE estim='sigma_10' AND type='tournament_2' AND
                              L IN (10, 20, 80, 100, 200) AND N IN (100, 200) GROUP BY l*n
                        ORDER BY l * n 
                        """

            df = sqlio.read_sql_query(sql, conn)
            data = df.to_numpy()

            s10, = plt.plot(data[:, 0], data[:, 1], c='springgreen', label='sigma_10')

            sql = f"""
               SELECT l * n, AVG(final_px)
               FROM final_pxs_extended
               WHERE estim='l-hamming_d' AND type='tournament_2' AND
                     L IN (10, 20, 80, 100, 200, 800, 1000, 2000) AND N IN (100, 200)
                GROUP BY l*n
               ORDER BY l * n
               """

            df = sqlio.read_sql_query(sql, conn)
            data = df.to_numpy()

            d2, = plt.plot(data[:, 0], data[:, 1], c='r', label='l-hamming_d')
            plt.legend(handles=[s2, s4, s10, d2])
            plt.xlabel('L*N')
            plt.ylabel('Pmax')
            plt.title("Toournament 2")

        def compare_inits():
            sql = f"""
            SELECT l * n, AVG(final_px)
            FROM final_pxs_extended
            WHERE estim='l-hamming_d' AND type='rws' AND init='uniform' AND
                  L IN (10, 20, 80, 100, 200) AND N IN (100, 200) GROUP BY l * n
            ORDER BY l * n
            """

            df = sqlio.read_sql_query(sql, conn)
            data = df.to_numpy()

            ham, = plt.plot(data[:,0], data[:,1], c='r', label='uniform')

            sql = f"""
               SELECT l * n, AVG(final_px)
               FROM final_pxs_extended
               WHERE estim='l-hamming_d' AND type='rws' AND init='all_0' AND
                     L IN (10, 20, 80, 100, 200, 800, 1000, 2000) AND N IN (100, 200) GROUP BY l * n
               ORDER BY l * n
               """

            df = sqlio.read_sql_query(sql, conn)
            data = df.to_numpy()

            d2, = plt.plot(data[:, 0], data[:, 1], c='b', label='all_0')

            sql = f"""
               SELECT l * n, AVG(final_px)
               FROM final_pxs_extended
               WHERE estim='l-hamming_d' AND type='rws' AND init='normal' AND
                     L IN (10, 20, 80, 100, 200, 800, 1000, 2000) AND N IN (100, 200) GROUP BY l * n
               ORDER BY l * n
               """

            df = sqlio.read_sql_query(sql, conn)
            data = df.to_numpy()

            d4, = plt.plot(data[:, 0], data[:, 1], c='teal', label='normal')

            plt.legend(handles=[ham, d2, d4])
            plt.xlabel('L*N')
            plt.ylabel('Pmax')
            plt.title("RWS")

        def scatter_lines():
            sql = f"""
                SELECT l * n, final_px
                FROM final_pxs_extended
                WHERE estim='l-hamming_d' AND type='rws' AND init='uniform' 
        --             AND L IN (10, 20, 80, 100, 200, 800, 1000, 2000) AND N IN (100, 200)
                ORDER BY l * n
                """

            df = sqlio.read_sql_query(sql, conn)
            data = df.to_numpy()
            a = plt.scatter(1 / data[:, 0], data[:, 1], c='b',s=5, label='rws')

            sql = f"""
                    SELECT l * n, final_px
                    FROM final_pxs_extended
                    WHERE estim='l-hamming_d' AND type='tournament_4' AND init='uniform' 
            --             AND L IN (10, 20, 80, 100, 200, 800, 1000, 2000) AND N IN (100, 200)
                    ORDER BY l * n
                    """

            df = sqlio.read_sql_query(sql, conn)
            data = df.to_numpy()
            c = plt.scatter(1 / data[:, 0], data[:, 1], c='teal',s=5, label='tournament_4')

            sql = f"""
                    SELECT l * n, final_px
                    FROM final_pxs_extended
                    WHERE estim='l-hamming_d' AND type='tournament_12' AND init='uniform' 
            --             AND L IN (10, 20, 80, 100, 200, 800, 1000, 2000) AND N IN (100, 200)
                    ORDER BY l * n
                    """

            df = sqlio.read_sql_query(sql, conn)
            data = df.to_numpy()
            d = plt.scatter(1 / data[:, 0], data[:, 1], c='springgreen',s=5, label='tournament_12')

            sql = f"""
                    SELECT l * n, final_px
                    FROM final_pxs_extended
                    WHERE estim='l-hamming_d' AND type='tournament_2' AND init='uniform' 
            --             AND L IN (10, 20, 80, 100, 200, 800, 1000, 2000) AND N IN (100, 200)
                    ORDER BY l * n
                    """

            df = sqlio.read_sql_query(sql, conn)
            data = df.to_numpy()
            b = plt.scatter(1 / data[:, 0], data[:, 1], c='g', s=5, label='tournament_2')

            plt.legend(handles=[a, b, c, d])
            plt.show()

        def plot():
            sql = f"""
            SELECT l * n, final_px
            FROM final_pxs_extended
            WHERE estim='l-hamming_d' AND type='rws' AND init='uniform' AND
                  L IN (10, 20, 80, 100, 200, 800, 1000, 2000) AND N IN (100, 200)
            ORDER BY l * n
            """

            df = sqlio.read_sql_query(sql, conn)
            data = df.to_numpy()

            ham, = plt.plot(data[:,0], data[:,1], c='r', label='rws')

            sql = f"""
               SELECT l * n, final_px
               FROM final_pxs_extended
               WHERE estim='l-hamming_d' AND type='tournament_2' AND init='uniform' AND
                     L IN (10, 20, 80, 100, 200, 800, 1000, 2000) AND N IN (100, 200)
               ORDER BY l * n
               """

            df = sqlio.read_sql_query(sql, conn)
            data = df.to_numpy()

            d2, = plt.plot(data[:, 0], data[:, 1], c='b', label='tournament_2')

            sql = f"""
               SELECT l * n, final_px
               FROM final_pxs_extended
               WHERE estim='l-hamming_d' AND type='tournament_4' AND init='uniform' AND
                     L IN (10, 20, 80, 100, 200, 800, 1000, 2000) AND N IN (100, 200)
               ORDER BY l * n
               """

            df = sqlio.read_sql_query(sql, conn)
            data = df.to_numpy()

            d4, = plt.plot(data[:, 0], data[:, 1], c='teal', label='tournament_4')

            sql = f"""
               SELECT l * n, final_px
               FROM final_pxs_extended
               WHERE estim='l-hamming_d' AND type='tournament_12' AND init='uniform' AND
                     L IN (10, 20, 80, 100, 200, 800, 1000, 2000) AND N IN (100, 200)
               ORDER BY l * n
               """

            df = sqlio.read_sql_query(sql, conn)
            data = df.to_numpy()

            d10, = plt.plot(data[:, 0], data[:, 1], c='springgreen', label='tournament_12')
            plt.legend(handles=[ham, d2, d4, d10])
            plt.title("Selection")

        compare_inits()
        plt.show()


if __name__ == '__main__':
    main()