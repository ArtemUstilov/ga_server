from typing import List

from core.mutation import mutate
from database import AggrRecord, Session, TestQueueRecord, AggrRecordTest, AggrTestDetails
from task.constants import INIT_MAP, ESTIMATION_MAP, SELECTION_MAP, N_IT, EPS, STOP_COUNT, \
    NUM_PROGONS_TEST
from utils import simple_polymorphous, locus_roles_polymorphous


def run_one_simulation(
    init_func: callable,
    estimation_func: callable,
    selection_func: callable,
    l: int,
    n: int,
    px: float,
):
    kwargs = {}

    pop = init_func(n, l, **kwargs)
    health = estimation_func(pop, **kwargs)

    # Start loop
    last_mean_health = health.mean()
    final_iter_num = N_IT - 1
    last_counter = 0
    poly_d1 = []
    mean_health_ar = []

    for i in range(0, N_IT):
        pop = selection_func(pop, health, n)
        pop = mutate(pop, px)
        health = estimation_func(pop, **kwargs)
        mean_health = health.mean()
        mean_health_ar.append(mean_health)

        if abs(last_mean_health - mean_health) < EPS:
            last_counter += 1
        else:
            last_counter = 0
        if last_counter >= STOP_COUNT:
            final_iter_num = i
            break

        last_mean_health = mean_health
        if 'good' in kwargs:
            poly_d1.append(locus_roles_polymorphous(pop, **kwargs))
        else:
            poly_d1.append(simple_polymorphous(pop))

    return final_iter_num, mean_health_ar, poly_d1


def run_record(
    init: str,
    estim: str,
    sel_type: str,
    l: int,
    n: int,
    px: float,
    progons: list,
    note: str
):
    session = Session()
    init_func = INIT_MAP[init]
    estimation_func = ESTIMATION_MAP[estim]
    selection_func = SELECTION_MAP[sel_type]
    run_results = []
    mean_h_ar = []
    poly_p1s = []
    count_successful = 0

    for _ in progons:
        res = run_one_simulation(init_func, estimation_func, selection_func, l, n, px)
        successful, mean_health, poly_p1 = res
        run_results.append(successful)
        mean_h_ar.append(mean_health)
        poly_p1s.append(poly_p1)
        if successful + 1 < N_IT:
            count_successful += 1

    rec = AggrRecord(
        L=l,
        N=n,
        init=init,
        estim=estim,
        type=sel_type,
        cur_px=px,
        runs_final=run_results,
        count_succ=count_successful,
        note=note,
    )

    session.add(rec)
    session.commit()


def run_test(queue_record: TestQueueRecord):
    session = Session()
    record: AggrRecord = session.query(AggrRecord).get(queue_record.record_id)

    kwargs = {
        'init_func': INIT_MAP[record.init],
        'estimation_func': ESTIMATION_MAP[record.estim],
        'selection_func': SELECTION_MAP[record.type],
        'l': record.L,
        'n': record.N,
    }
    instance = AggrRecordTest(
        record_id=record.id,
        L=record.L,
        N=record.N,
        init=record.init,
        estim=record.estim,
        type=record.type,
    )

    px = record.cur_px * queue_record.coef
    details:List[AggrTestDetails] = []

    for test_case, suffix in [(0.8, '_80'), (1, ''), (1.2, '_120')]:
        count_successful = 0
        run_results = []
        mean_h_ar = []
        poly_p1s = []
        cur_px = test_case * px
        setattr(instance, 'test_px' + suffix, cur_px)

        for j in range(NUM_PROGONS_TEST):
            res = run_one_simulation(**kwargs, px=cur_px)
            successful, mean_health, poly_p1 = res

            run_results.append(successful)
            mean_h_ar.append(mean_health)
            poly_p1s.append(poly_p1)

            if successful + 1 < N_IT:
                count_successful += 1

            details.append(AggrTestDetails(
                percent=int(test_case * 100),
                run_number=j,
                mean_health=mean_h_ar,
                polymorphous1_p=poly_p1s
            ))

        setattr(instance, 'runs_final' + suffix, run_results)
        setattr(instance, 'count_succ' + suffix, count_successful)

    session.add(instance)
    session.commit()

    for d in details:
        d.test_record_id = instance.id
        session.add(d)

    session.commit()
