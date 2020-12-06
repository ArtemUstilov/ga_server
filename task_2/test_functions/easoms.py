import numpy as np


def easoms_function_2(pop_decoded_1: np.ndarray, pop_decoded_2: np.ndarray, *args,
                      **kwargs) -> np.ndarray:
    x_expr_1 = np.cos(pop_decoded_1) * np.cos(pop_decoded_2)
    x_expr_2 = - (pop_decoded_1 - np.pi) ** 2 - (pop_decoded_2 - np.pi) ** 2
    return x_expr_1 * np.exp(x_expr_2)

#
# # Visualize
# import matplotlib.pyplot as plt
# from mpl_toolkits import mplot3d
#
# x1 = np.arange(-100, 100, 0.1, dtype=np.float32)
# x2 = np.arange(-100, 100, 0.1, dtype=np.float32)
# y = easoms_function_2(x1, x2)
#
# ax = plt.axes(projection='3d')
# ax.plot_trisurf(y, x2, x1,
#                 )
# plt.show()
