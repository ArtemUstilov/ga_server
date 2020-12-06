import numpy as np


def ackleys_function_1(pop_decoded: np.ndarray, *args, **kwargs) -> np.ndarray:
    x_expr_1 = -0.2 * np.abs(pop_decoded)
    x_expr_2 = np.cos(2 * np.pi * pop_decoded)
    return 20 * np.exp(x_expr_1) + np.exp(x_expr_2) - 20 - np.e


# Visualize
# import matplotlib.pyplot as plt
# x = np.arange(-32768, 32768, dtype=np.float32)/1000
# y = ackleys_function_1(x)
# plt.plot(x, y, c='blue')
# plt.show()
