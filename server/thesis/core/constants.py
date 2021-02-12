from .count_next_population_sizes import next_population_size_type_1, next_population_size_type_2, \
    next_population_size_type_3, next_population_size_type_4, next_population_size_type_3_init_200, \
    next_population_size_type_3_init_200_increase_from_500
from .estimation import const as all_l, on_split_locuses
from .initialization import all_zeros as all_0, normal_with_locuses as normal
from .selection import roulette as rws, tournament_2, tournament_4, tournament_12

EPS = 0.0001
N_IT = 20000

INIT_MAP = {
    'all_0': all_0,
    'normal': normal,
}

ESTIM_MAP = {
    'all_l': all_l,
    'on_split_locuses': on_split_locuses,
}

SELECTION_MAP = {
    'rws': rws,
    'tournament_2': tournament_2,
    'tournament_4': tournament_4,
    'tournament_12': tournament_12,
}

SIZE_POP = {
    'type_1': next_population_size_type_1,
    'type_2': next_population_size_type_2,
    'type_3': next_population_size_type_3,
    'type_4': next_population_size_type_4,
    'type_3_init_200': next_population_size_type_3_init_200,
    'type_3_i_200_px0_1': next_population_size_type_3_init_200,
    'type_3_i_200_px10': next_population_size_type_3_init_200,
    'type_3_i_200_if_500': next_population_size_type_3_init_200_increase_from_500,
}

N_POP = {
    'type_1': 1000,
    'type_2': 2000,
    'type_3': 2000,
    'type_4': 2000,
    'type_3_init_200': 2000,
    'type_3_i_200_px10': 2000,
    'type_3_i_200_px0_1': 2000,
    'type_3_i_200_if_500': 2000,
}

cols_info = [
    'N',
    'iteration',
    'pairwise_hamming_distribution_p',
    'pairwise_hamming_distribution_abs',
    'ideal_hamming_distribution_p',
    'ideal_hamming_distribution_abs',
    'wild_type_hamming_distribution_p',
    'wild_type_hamming_distribution_abs',

    'expected_value_pair',
    'std_pair',
    'expected_value_ideal',
    'std_ideal',
    'expected_value_wild',
    'std_wild',

    'min_pair',
    'max_pair',
    'min_ideal',
    'max_ideal',
    'min_wild',
    'max_wild',

    'variance_coef_pair',
    'variance_coef_ideal',
    'variance_coef_wild',

    'mode_pair',
    'mode_ideal',
    'mode_wild',

    'health',
    'mean_health',
    'mean_health_diff_0',
    'best_health_diff_0',

    'polymorphism',
    'ga_run_settings_id',
    'last_iter'
]

cols_settings = [
    'id',
    'init',
    'estim',
    'sel_type',
    'size_pop_type',
    'L',
    'run_id'
]

conn_str = "dbname=%s host=%s port=%d user=%s password=%s" % \
           ("thesis", "localhost", 5432, "artemustilov", "")

#http://127.0.0.1:8000/thesis/run?size_pop_type=type_1&l=10&px=0.1&runs=1&init=all_0&estim=all_l&sel_type=rws