from .estimation import const as all_l, two_const, sigma, inverted_hamming_distance, hamming_distance
from .initialization import all_zeros as all_0, all_ones as all_1, half_zeros_half_ones as half_0_half_1,all_1_one_0, normal, \
    normal_with_ideal
from .selection import roulette as rws, tournament_gen, sus, uniform, not_linear_rang, linear_rang, cutting_selection, \
    exp_rang, roulette_destroy, roulette_linear, roulette_mixed, roulette_power, roulette_sigma, \
    tournament_without_return_gen

INIT_MAP = {
    'all_0': all_0,
    'all_1': all_1,
    'all_1_one_0': all_1_one_0,
    'half_1_half_0': half_0_half_1,
    'normal': normal,
    'normal_with_ideal': normal_with_ideal,
}

ESTIM_MAP = {
    'all_l': all_l,
    'two_const': two_const,
    'sigma': sigma,
    'hamming': hamming_distance,
    'inv_hamming': inverted_hamming_distance,
}

SELECTION_MAP = {
    'rws': rws,
    'roulette_linear': roulette_linear,
    'roulette_sigma': roulette_sigma,
    'roulette_power': roulette_power,
    'roulette_destroy': roulette_destroy,
    'roulette_mixed': roulette_mixed,
    'sus': sus,
    'tournament': tournament_gen,
    'tournament_without_return_gen': tournament_without_return_gen,
    'cutting_selection': cutting_selection,
    'linear_rang': linear_rang,
    'not_linear_rang': not_linear_rang,
    'exp_rang': exp_rang,
    'uniform': uniform,
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

    'ga_run_settings_id',
    'last_iter',
    'best_health',
    'amount_bests',
    'taken_to_next',
    'diff_prev',
    'intensity_prev',
    'diff_prev_amount_bests',
    'genotype',
]

cols_settings = [
    'id',
    'init',
    'estim',
    'sel_type',
    'L',
    'N',
    'px',
    'use_mutation',
    'run_id',
    'const_1', 'const_2', 'sigma', 'sel_param1', 'sel_param2', 'title'
]

conn_str = "dbname=%s host=%s port=%d user=%s password=%s" % \
           ("thesis", "localhost", 5432, "artemustilov", "")
