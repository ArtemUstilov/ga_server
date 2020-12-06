import numpy as np


def spherical_function_1(pop_decoded: np.ndarray, a: float, *args, **kwargs) -> np.ndarray:
    return a * a - pop_decoded ** 2


# # Visualize
# import matplotlib.pyplot as plt
# x = np.arange(-512, 512, dtype=np.float32)/100
# y = spherical_function_1(x, 5.12)
# plt.plot(x, y, c='blue')
# plt.show()
