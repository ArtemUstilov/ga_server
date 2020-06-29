import itertools
import logging
from concurrent.futures.thread import ThreadPoolExecutor
from typing import List

from database import Session, TestQueueRecord
from task.constants import TRY_NUM, NUM_PROGONS, INIT_L_SCALE, N_IT, STOP_COUNT, EPS
from task.task import run_record

logger = logging.getLogger(__name__)


def run_parameters(
    inits: List[str],
    estims: List[str],
    sel_types: List[str],
    ls: List[int],
    ns: List[int],
    algos: List[str],
):
    params = itertools.product(inits, estims, sel_types, ls, ns, algos)
    with ThreadPoolExecutor(max_workers=20) as executor:
        for (init, estim, sel_type, l, n, algo) in params:
            param = {
                'init': init,
                'estim': estim,
                'sel_type': sel_type,
                'l': l,
                'n': n,
                'algo': algo,
                'NUM_PROGONS': NUM_PROGONS,
                'TRY_NUM': TRY_NUM,
                'INIT_L_SCALE': INIT_L_SCALE,
                'N_IT': N_IT,
                'STOP_COUNT': STOP_COUNT,
                'EPS': EPS
            }
            executor.submit(run_helper, param)


def run_helper(params):
    logger.info(f'Starting with params: {params}')
    if params['algo'] == 'run_param_set':
        run_param_set(**params)
    elif params['algo'] == 'run_param_set_v2':
        run_param_set_v2(**params)
    logger.info(f'Finished with params: {params}')


def run_param_set(
    init: str,
    estim: str,
    sel_type: str,
    l: int,
    n: int,
    **kwargs
):
    session = Session()
    last_success = None
    px = 1 / (INIT_L_SCALE * l)
    sigma = px * 0.5
    progons = list(range(NUM_PROGONS))
    for try_id in range(TRY_NUM):
        record = run_record(init, estim, sel_type, l, n, px, try_id, progons, '', session,
                            'run_param_set')
        if record.count_succ == NUM_PROGONS:
            px += sigma
            last_success = record
        else:
            px -= sigma
        sigma = sigma * 0.5

    if last_success:
        last_success.chosen_for_test = True
        session.commit()
    else:
        logger.error(f'Failed to run for params {(init, estim, sel_type, l, n)}')


def run_param_set_v2(
    init: str,
    estim: str,
    sel_type: str,
    l: int,
    n: int,
):
    session = Session()
    last_success = None
    left = 0
    right = 1
    px = (left + right) / (INIT_L_SCALE * l)
    progons = list(range(NUM_PROGONS))
    for try_id in range(TRY_NUM):
        record = run_record(init, estim, sel_type, l, n, px, try_id, progons, '', session,
                            'run_param_set_v2')
        if record.count_succ == NUM_PROGONS:
            left = px
            last_success = record
        else:
            right = px
        px = (left + right) / 2

    if last_success:
        last_success.chosen_for_test = True
        session.add(TestQueueRecord(
            record_id=last_success.id
        ))
        session.commit()
    else:
        logger.error(f'Failed to run for params {(init, estim, sel_type, l, n)}')

