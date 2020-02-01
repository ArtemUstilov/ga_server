from time import sleep

import pandas as pd

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

FILE_NAME = 'out/task1/task1_id_8_L_100_N_100_px_0.0010.csv'
fig = plt.figure()

file = pd.read_csv(FILE_NAME)
L = 50
hist = file[[f'D_{i}' for i in range(L)]].to_numpy(dtype=np.float64)
max_val = hist.max()


def update(val):
    val = int(val)
    ax.cla()
    ax.plot(0, 0, 0, max_val)
    ax.bar(np.arange(L), height=hist[val])
    plt.draw()


def on_click(event):
    for i in range(0, 210):
        slider_it.set_val(i)
        fig.canvas.draw()
        sleep(0.001)


ax = plt.subplot(111)
plt.subplots_adjust(left=0.25, bottom=0.25)

ax.bar(np.arange(L), height=hist[0])

axit = plt.axes([0.25, 0.01, 0.65, 0.03])
slider_it = Slider(axit, 'Iteration', valinit=0, valstep=1, valmin=0, valmax=209)

slider_it.on_changed(update)
axcut = plt.axes([0.9, 0.1, 0.1, 0.075])
bcut = Button(axcut, 'Run')
bcut.on_clicked(on_click)

plt.show()
