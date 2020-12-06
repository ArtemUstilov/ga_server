import numpy as np


def griwangks_function_1(pop_decoded: np.ndarray, a: float, *args, **kwargs) -> np.ndarray:
    s = (pop_decoded ** 2) / 4000
    p = np.cos(pop_decoded) + 1
    return 1 - s - p


# # Visualize
# import matplotlib.pyplot as plt
# x = np.arange(-60000, 60000, dtype=np.float32)/100
# y = griwangks_function_1(x, 600)
# plt.plot(x, y, c='blue')
# plt.show()
