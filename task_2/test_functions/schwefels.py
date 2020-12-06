import numpy as np


def schwefels_function_1(pop_decoded: np.ndarray, *args, **kwargs) -> np.ndarray:
    x_expr = np.sqrt(np.abs(pop_decoded))
    return pop_decoded * np.sin(x_expr)


# Visualize
import matplotlib.pyplot as plt
x = np.arange(-50000, 50000, dtype=np.float32)/100
y = schwefels_function_1(x)
plt.plot(x, y, c='blue')
plt.show()
