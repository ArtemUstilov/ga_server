from task_2.mappers import TEST_FUNC_MAP
from task_2.models import ParamSet


def get_estimation_function(param_set: ParamSet):
    alias = param_set.func_case.function.alias

    dim_n = param_set.func_case.func_param.dim_n
    a = param_set.func_case.func_param.interval_a
    b = param_set.func_case.func_param.interval_b

    if dim_n == 1:
        return lambda pop_decoded: TEST_FUNC_MAP[alias](pop_decoded, a, b)
    else:
        raise NotImplementedError


def get_stop_cond_params(param_set: ParamSet):
    s = param_set.stop_cond
    return s.get('steps_back', 10), s.get('MAX_NFE', 10000000),  s.get('EPS', 0.0001)
