import task_2.test_functions as f
import task_2.helpers.constants as const

from core.initialization import uniform
from core.selection import roulette, tournament_2, tournament_4, tournament_12

# TODO ask uniform
INIT_MAP = {
    const.UNIFORM_INIT: uniform
}

SEL_TYPE_MAP = {
    const.RWS_SEL: roulette,
    const.TOURNAMENT_2_SEL: tournament_2,
    const.TOURNAMENT_4_SEL: tournament_4,
    const.TOURNAMENT_12_SEL: tournament_12,
    # TODO sus sel type
    const.SUS_SEL: None,
}


TEST_FUNC_MAP = {
    'achleys': f.ackleys_function_1,
    'debs': f.debs_function_1,
    'griwangks': f.griwangks_function_1,
    'rastrigins': f.rastrigins_function_1,
    'schwefels': f.schwefels_function_1,
    'spherical': f.spherical_function_1,
    'uneven_debs': f.uneven_debs_function_1,
}
