import numpy as np


def uneven_debs_function_1(pop_decoded: np.ndarray, *args, **kwargs) -> np.ndarray:
    x_expr = ((pop_decoded-0.08)/0.854) ** 2
    sin_part = (np.sin(5 * np.pi * (pop_decoded ** 0.75 - 0.05))) ** 6
    return np.e ** (-2 * np.log(2) * x_expr) * sin_part


# # Visualize
# import matplotlib.pyplot as plt
# x = np.arange(1,1000, dtype=np.float32)/1000
# y = uneven_debs_function_1(x)
# plt.plot(x, y, c='blue')
# plt.show()
