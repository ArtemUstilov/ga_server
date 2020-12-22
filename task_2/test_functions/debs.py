import numpy as np


def debs_function_1(pop_decoded: np.ndarray, *args, **kwargs) -> np.ndarray:
    x_expr = ((pop_decoded-0.1)/0.8) ** 2
    return np.e ** (-2 * np.log(2) * x_expr) * (np.sin(5 * np.pi * pop_decoded)) ** 6


# # Visualize
# import matplotlib.pyplot as plt
# x = np.arange(1,1000, dtype=np.float32)/1000
# y = debs_function_1(x)
# plt.plot(x, y, c='blue')
# plt.show()
