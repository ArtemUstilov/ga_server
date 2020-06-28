import numpy as np
import pandas as pd
import os

# len = 12
BASE_PROPS = [
    'num_ind',
    'distance',
    'expected_value',
    'std_deviation',
    'mode',
    '%_of_neutral_with_one',
    '%_of_neutral_with_many',
    '%_of_neutral_with_many',
    'wild_type_%',
    'wild_type_abs',
    'mean_health_diff_0',
    'best_health_diff_0',
]


def get_props(num_locuses):
    distances = [
        f'distance_{i}' for i in range(num_locuses+1)
    ]

    return BASE_PROPS + distances


def write_file(name, dataframe):
    path = os.path.join(os.curdir, 'out')
    if not os.path.exists(path):
        os.mkdir(path)
    path = os.path.join(path, f'{name}.csv')
    dataframe.to_csv(path, index=False)



def create_empty_frame(num_locuses, num_max_iter):
    cols = get_props(num_locuses)
    z = np.zeros((num_max_iter, len(cols)), dtype=np.int8)
    return pd.DataFrame(z, columns=cols)
