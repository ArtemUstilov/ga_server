import numpy as np

from task_2.helpers.constants import BIN_ENCODING, GRAY_ENCODING


def bin_to_dec(arr: np.ndarray) -> np.ndarray:
    L = arr.shape[1]
    # [2**(L-1), 2**(L-2), ..., 1]
    p = 2 ** np.arange(L-1, -1, -1, dtype=np.uint64)

    return (arr * p).sum(axis=1).astype(np.uint64)


def dec_to_bin(arr: np.ndarray, L: int) -> np.ndarray:
    # [2**(L-1), 2**(L-2), ..., 1]
    p = (2 ** np.arange(L - 1, -1, -1)).astype(np.uint64)

    return ((arr & p) != 0).astype(np.uint8)


def gray_to_dec(arr: np.ndarray) -> np.ndarray:
    N = arr.shape[0]
    d = bin_to_dec(arr)

    inv = np.zeros(N, dtype=d.dtype)
    while np.any(d):
        inv = inv ^ d
        d = d >> 1

    return inv


def dec_to_gray(arr: np.ndarray, L: int) -> np.ndarray:
    nums = (arr >> 1) ^ arr
    return dec_to_bin(nums, L)


def encode(pop: np.ndarray, L: int, coder_info: dict):
    """

    :param pop: array like [[31.1] [1.0] [11] ... dtype=np.float64]
    :param L: length of inds
    :param coder_info: param info
    :return: array like [[1 0 1 0 1 1 0 1 1 0] [1 0 0 0 0 1 1 0 1 0] ... dtype=np.int8]
    """
    a = coder_info['a']
    b = coder_info['b']

    nums = (pop - a) / (b - a) * (2 ** L - 1)
    nums = nums.round().astype(np.uint64)

    algo = coder_info['type']
    if algo == BIN_ENCODING:
        return dec_to_bin(nums, L)
    elif algo == GRAY_ENCODING:
        return dec_to_gray(nums, L)
    else:
        raise ValueError(f'Coding algorithm {algo} not recognized')


def decode(pop: np.ndarray, L:int, coder_info: dict):
    """

    :param pop: array like  [[1 0 1 0 1 1 0 1 1 0] [1 0 0 0 0 1 1 0 1 0] ... dtype=np.int8]
    :param L: length of inds
    :param coder_info: param info
    :return: array like [[31.1] [1.0] [11] ... dtype=np.float64]
    """

    algo = coder_info['type']
    if algo == BIN_ENCODING:
        nums = bin_to_dec(pop)
    elif algo == GRAY_ENCODING:
        nums = gray_to_dec(pop)
    else:
        raise ValueError(f'Coding algorithm {algo} not recognized')

    a = coder_info['a']
    b = coder_info['b']

    return a + nums * (b - a) / (2 ** L - 1)
