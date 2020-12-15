import math

from task_2.helpers.constants import BIN_ENCODING, UNIFORM_INIT, RWS_SEL
from task_2.models import FuncCase, ParamSet


def generate_param_set(func_case: FuncCase, **kwargs):
    params = {
        'encoding': {
            'type': BIN_ENCODING
        },
        'init': UNIFORM_INIT,
        'sel_type': RWS_SEL,
        'N': 100,
        'stop_code': {
            'steps_back': 10,
            'MAX_NFE': 10000000,
            'EPS': 0.0001,
        },
        'num_runsets': 15,
        'num_runs': 10,
        'crossover_pc': 0.5,
        'func_case': func_case
    }

    params.update(kwargs)

    p = func_case.func_param
    num_intervals = (p.interval_a - p.interval_b) / 10 ** p.accuracy_decimals
    l_val = math.log2(num_intervals)

    if not l_val.is_integer():
        raise ValueError('Incorrect FuncParam')

    params['L'] = int(l_val)
    ps = ParamSet(**params)
    ps.save()
