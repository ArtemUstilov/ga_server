import numpy as np


def rastrigins_function_1(pop_decoded: np.ndarray, a:float, *args, **kwargs) -> np.ndarray:
    return (10 * np.cos(2 * np.pi * pop_decoded) - pop_decoded**2) - 10


# # Visualize
# import matplotlib.pyplot as plt
# x = np.arange(-512, 512, dtype=np.float32)/100
# y = rastrigins_function_1(x, 5.12)
# plt.plot(x, y, c='blue')
# plt.show()
