from core import initialization, estimation, selection

EPS = 0.0001
N_IT = 20000
STOP_COUNT = 10
NUM_PROGONS_TEST = 5

INIT_MAP = {
    'all_0': initialization.all_zeros,
    'uniform': initialization.uniform,
    'normal': initialization.normal,
    'normal_with_loc': initialization.normal_with_locuses,
}

ESTIMATION_MAP = {
    'all_l': estimation.const,
    'l-hamming_d': estimation.inverted_hamming_distance,
    'on_split_loc': estimation.on_split_locuses,
    'sigma_2': estimation.sigma_2,
    'sigma_4': estimation.sigma_4,
    'sigma_10': estimation.sigma_10,
}

SELECTION_MAP = {
    'rws': selection.roulette,
    'tournament_2': selection.tournament_2,
    'tournament_4': selection.tournament_4,
    'tournament_12': selection.tournament_12,
}
