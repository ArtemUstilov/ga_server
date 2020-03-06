from time import sleep

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.widgets import Slider, Button, TextBox

pause = True
it = 0


def show_diagram(cursor, l, n, sel_type):
    sql = f"""
    SELECT iteration, pairwise_hamming_distribution_p, 
                        wild_type_hamming_distribution_p, 
                        ideal_hamming_distribution_p
    FROM task2_full_v1
    WHERE L={l} AND N={n} AND sel_type='{sel_type}' AND run_id=0
    ORDER BY iteration
    """

    cursor.execute(sql)
    rows = cursor.fetchall()
    hist = np.array([row[1] for row in rows])
    hist2 = np.array([row[2] for row in rows])
    hist3 = np.array([row[3] for row in rows])

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1)
    barcollection = ax1.bar(range(l), hist[0])
    barcollection2 = ax2.bar(range(l), hist2[0])
    barcollection3 = ax3.bar(range(l), hist3[0])

    axcut = plt.axes([0.1, 0.9, 0.1, 0.075])
    tcut = TextBox(axcut, 'Iter:', '0')

    axcut2 = plt.axes([0.25, 0.9, 0.1, 0.06])
    bcut = Button(axcut2, 'Run')

    def simData():
        global it
        while it < len(rows):
            if not pause:
                it += 1
            yield it

    def onClick(event):
        bcut.label.set_text('Stop')
        tcut.stop_typing()
        global pause
        pause ^= True

    def simPoints(it):
        if not pause:
            tcut.set_val(str(it))

        for i, (b, b1, b2) in enumerate(zip(barcollection, barcollection2, barcollection3)):
            b.set_height(hist[it, i])
            b1.set_height(hist2[it, i])
            b2.set_height(hist3[it, i])
        # return barcollection

    def change_it(event):
        global it
        it = int(event)

    tcut.on_submit(change_it)
    bcut.on_clicked(onClick)
    fig.set_size_inches(18.5, 10.5)
    ani = animation.FuncAnimation(fig, simPoints, simData, blit=False, interval=10,
                                  repeat=True)
    plt.show()


def save_diagrams(cursor, l, n, sel_type):
    sql = f"""
    SELECT iteration, pairwise_hamming_distribution_p, 
                        wild_type_hamming_distribution_p, 
                        ideal_hamming_distribution_p,
                        
                        expected_value_pair, expected_value_wild, expected_value_ideal,
                        std_pair, std_wild, std_ideal,
                        variance_coef_pair, variance_coef_wild, variance_coef_ideal,
                        mode_pair, mode_wild, mode_ideal,
                        min_pair, max_pair, min_wild, max_wild, min_ideal, max_ideal,

                        mean_health, mean_health_diff_0, best_health_diff_0
    FROM task2_full_v1
    WHERE L={l} AND N={n} AND sel_type='{sel_type}' AND run_id=0
    ORDER BY iteration
    LIMIT 100
    """
    cursor.execute(sql)
    rows = cursor.fetchall()
    hist = np.array([row[1] for row in rows])
    hist2 = np.array([row[2] for row in rows])
    hist3 = np.array([row[3] for row in rows])

    for it in range(100):
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1)
        ax1.set_ylim([0, 1])
        ax2.set_ylim([0, 1])
        ax3.set_ylim([0, 1])
        # fig.set_tight_layout(True)

        plt.subplots_adjust(left=0.05, bottom=0.02, right=0.85, top=0.98, wspace=0.78, hspace=0.1)
        barcollection = ax1.bar(range(l), hist[it])
        barcollection2 = ax2.bar(range(l), hist2[it], color='r')
        barcollection3 = ax3.bar(range(l), hist3[it], color='g')

        axcut = plt.axes([0.9, 0.95, 0.1, 0.05])
        tcut = TextBox(axcut, 'Iter:', f'{it}')

        fig.set_size_inches(18.5, 8.5)
        ax1.text(110, 0.05,
                 f'Mean health: {rows[it][22]}\n'
                 f'Mean health diff 0: {rows[it][23]}\n'
                 f'Best health diff 0: {rows[it][24]}', color='b')
        ax1.text(105, 0.5,
                 f'PAIRWISE\n'
                 f'E:{rows[it][4]}\nStd:{rows[it][7]}\nVariance coef:{rows[it][10]}\nmode:{rows[it][13]}\n'
                 f'Min:{rows[it][16]}   Max:{rows[it][17]}')
        ax2.text(105, 0.5,
                 f'WILD TYPE\n'
                 f'E:{rows[it][5]}\nStd:{rows[it][8]}\nVariance coef:{rows[it][11]}\nmode:{rows[it][14]}\n'
                 f'Min:{rows[it][18]}   Max:{rows[it][19]}')
        ax3.text(105, 0.5,
                 f'IDEAL\n'
                 f'E:{rows[it][6]}\nStd:{rows[it][9]}\nVariance coef:{rows[it][12]}\nmode:{rows[it][15]}\n'
                 f'Min:{rows[it][20]}   Max:{rows[it][21]}')

        plt.savefig(f'./results/diagrams/l_100_it_{it}.png')
        plt.close(fig)
