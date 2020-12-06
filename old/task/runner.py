import logging
from concurrent.futures.thread import ThreadPoolExecutor

from old.database import Session, TestQueueRecord, pop_one_row, Params
from old.task.constants import TRY_NUM, NUM_PROGONS, INIT_L_SCALE, STOP_COUNT
from old.task.task import run_record

logger = logging.getLogger(__name__)


def run_parameters(limit=1):
    with ThreadPoolExecutor(max_workers=20) as executor:
        for _ in range(limit):
            executor.submit(run_helper)


def run_helper():
    params = pop_one_row(Params)
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
    progons = list(range(kwargs.get('NUM_PROGONS', NUM_PROGONS)))
    try_num = kwargs.get('TRY_NUM', TRY_NUM)
    stop_count = kwargs.get('STOP_COUNT', STOP_COUNT)
    for try_id in range(try_num):
        record = run_record(init, estim, sel_type, l, n, px, try_id, progons, '', session,
                            'run_param_set', stop_count, try_num)
        if record.count_succ == len(progons):
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
    **kwargs,
):
    session = Session()
    last_success = None
    left = 0
    right = 1
    px = (left + right) / (INIT_L_SCALE * l)
    progons = list(range(kwargs.get('NUM_PROGONS', NUM_PROGONS)))
    try_num = kwargs.get('TRY_NUM', TRY_NUM)
    stop_count = kwargs.get('STOP_COUNT', STOP_COUNT)
    for try_id in range(try_num):
        record = run_record(init, estim, sel_type, l, n, px, try_id, progons, '', session,
                            'run_param_set_v2', stop_count, try_num)
        if record.count_succ == len(progons):
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

