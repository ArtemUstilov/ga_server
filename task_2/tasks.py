import logging
from typing import Optional, List

import numpy as np

import task_2.mappers as mappers
from core.crossover import crossover
from core.mutation import mutate
from task_2.helpers.encoding import encode, decode
from task_2.helpers.constants import TESTING_FACTORS
from task_2.helpers.runner import get_estimation_function, get_stop_cond_params
from task_2.helpers.pmax import get_p_max
from task_2.helpers.run_results import (
    calculate_avg_test_results,
    calculate_best_test_results,
    calculate_best_run_set_results,
    calculate_avg_run_set_results,
)
from task_2.helpers.tasks import TaskType, create_task, remove_pending_task
from task_2.metrics.simple import hamming_distance_between
from task_2.models import (
    ParamSet,
    RunSet,
    Run,
    TestSuite,
    InitPopulation,
    ExperimentsSuite,
    Task,
)
from task_2.helpers.run_results import pairwise_hamming_distribution
from task_2.metrics.distributions import target_hamming_distribution

logger = logging.getLogger(__name__)


# Yup
def _schedule_tests(**test_kwargs):
    """
    Helping function to schedule tests

    :param test_kwargs: kwargs to pass to TestSuite obj
    :return: None
    """

    final_task = create_task(
        TaskType.FINALIZE_TEST_SUITE,
        [None]
    )
    pending = []
    kwargs = {
        'is_before': 'exp_suite_before' in test_kwargs
    }

    for factor in TESTING_FACTORS:
        test_suite = TestSuite(
            factor=factor,
            **test_kwargs
        )
        test_suite.save()
        task = create_task(
            TaskType.PROCESS_TEST_SUITE,
            test_suite_id=test_suite.id,
            finalize_id=final_task.id,
        )
        pending.append(task.id)
        kwargs[f'suite_{factor}'] = test_suite.id

    final_task.kwargs = kwargs
    final_task.pending_tasks = pending
    final_task.save()


# Yup
def create_exp_suite(task: Task, param_set_id: int):
    """
    Creates Exp suite for a particular ParamSet. Kicks off the process of experiment
    (schedules tests)

    :param task: Current task
    :param param_set_id: the id of corresponding ParamSet
    :return: None
    """

    logger.info('Take param set into work', extra={'data': {'param_set_id': param_set_id}})

    param_set = ParamSet.get_by_id(param_set_id)
    p_max = get_p_max(param_set.sel_type, param_set.L, param_set.N)
    exp_suite = ExperimentsSuite(
        p_start=p_max,
        param_set=param_set.id
    )
    exp_suite.save()
    _schedule_tests(
        init_pmax=p_max,
        exp_suite_before=exp_suite.id,
    )


# Yup
def process_test_suite(task: Task, test_suite_id: int, finalize_id: Optional[int] = None):
    """
    Runs any particular TestSuite.

    :param task: Current task
    :param test_suite_id: Id of corresponding TestSuite
    :param finalize_id: The id of task that can be run only after this task
    :return: None
    """

    suite: TestSuite = TestSuite.get_by_id(test_suite_id)

    if suite.exp_suite_before:
        param_set: ParamSet = suite.exp_suite_before.param_set
    else:
        param_set: ParamSet = suite.exp_suite_after.param_set

    logger.info('TestSuite taken into work', extra={'data': {'test_suite_id': test_suite_id}})

    count_successful = 0
    for run_num in range(param_set.num_runs):
        run = process_single_run(
            param_set,
            suite.init_pmax * suite.factor,
            run_num,
            test_suite_id=test_suite_id
        )

        if run.is_succ:
            count_successful += 1
        else:
            break

    suite.succ_num = count_successful
    suite.is_succ = count_successful == param_set.num_runs
    suite.save()
    if finalize_id:
        remove_pending_task(task.id, finalize_id)
    logger.info('TestSuite finished successfully', extra={'data': {'test_suite_id': test_suite_id}})


# Yup
def finalize_test_suites(task: Task, is_before: bool, **kwargs):
    """
    Summarizes results of tests and decides what to do next with them

    :param task: Current task
    :param is_before: are these tests run with the Pmax from equation or
    with Pmax found in experimental way
    :param kwargs: Info needed for the task
    :return: None
    """

    suite100 = TestSuite.get_by_id(kwargs['suite_1'])
    suite80 = TestSuite.get_by_id(kwargs['suite_0.8'])
    suite120 = TestSuite.get_by_id(kwargs['suite_1.2'])

    if is_before:
        assert suite80.exp_suite_before == suite100.exp_suite_before == suite120.exp_suite_before
        exp_suite = suite100.exp_suite_before
    else:
        assert suite80.exp_suite_after == suite100.exp_suite_after == suite120.exp_suite_after
        exp_suite = suite100.exp_suite_after

    if suite80.is_succ and suite100.is_succ and not suite120.is_succ:
        # In case, tests succeeded
        logger.info(
            'TestSuite succeeded. Setting Pmax to ExperimentsSuite',
            extra={'data': {'test_suite_id': suite100.id}}
        )
        suite100.is_approved = True
        suite80.is_approved = True
        suite120.is_approved = True
        exp_suite.param_set.action_log.append(
            f'Tested Pmax {suite100.init_pmax} '
            f'the result is: SUCCESS'
        )
        exp_suite.param_set.save()
        exp_suite.finall_succ_n = suite100.succ_num
        exp_suite.finall_succ_pmax = suite100.init_pmax
        exp_suite.save()

    else:
        # Tests did not succeed from the first time
        logger.info(
            'TestSuite failed. Creating task to find Pmax',
            extra={'data': {'test_suite_id': suite100.id}}
        )
        suite100.is_approved = False
        suite80.is_approved = False
        suite120.is_approved = False
        exp_suite.param_set.action_log.append(
            f'Tested Pmax {suite100.init_pmax} '
            f'the result is: FAIL'
        )
        exp_suite.param_set.save()
        create_task(
            TaskType.PROCESS_RUN_SET,
            exp_suite_id=exp_suite.id,
            init_pmax=suite100.init_pmax,
        )

    suite100.save()
    suite80.save()
    suite120.save()

    for suite_id in [suite80.id, suite100.id, suite120.id]:
        calculate_avg_test_results(suite_id)
        calculate_best_test_results(suite_id)


# Yup
def process_run_set(task: Task, exp_suite_id: int, init_pmax: float):
    exp_suite = ExperimentsSuite.get_by_id(exp_suite_id)
    param_set = exp_suite.param_set
    logger.info('Started creating RunSets', extra={'data': {'exp_suite_id': exp_suite_id}})

    px = init_pmax
    sigma = px * 0.5

    last_succ_run_set = None
    run_set_ids = []

    for runset_num in range(param_set.num_runsets):
        run_set = RunSet(try_number=runset_num, exp_suite=exp_suite)
        run_set.pmax = px

        # Logging
        count_successful = 0
        for run_num in range(param_set.num_runs):
            run = process_single_run(param_set, px, run_num)

            if run.is_succ:
                count_successful += 1
            else:
                break
        if count_successful == param_set.num_runs:
            last_succ_run_set = run_set
            px += sigma
        else:
            px -= sigma
        sigma = sigma * 0.5

        run_set.succ_num = count_successful
        run_set.is_succ = count_successful == param_set.num_runs
        run_set.save()
        run_set_ids.append(run_set.id)

    create_task(
        TaskType.FINALIZE_RUN_SET,
        run_set_ids=run_set_ids
    )

    param_set.action_log.append(
        f'Found Pmax {last_succ_run_set.pmax} '
        f'on runset number {last_succ_run_set.try_number} '
        f'with last successful run id {last_succ_run_set.id}. '
        f'Creating new TestSuite'
    )
    param_set.save()

    _schedule_tests(
        init_pmax=last_succ_run_set.pmax,
        exp_suite_after=exp_suite.id,
    )


def finalize_run_set(task: Task, run_set_ids: List[int]):
    """
    Calculate in parallel aggregated metrics for RunSet

    :param task: current task
    :param run_set_ids: list of ids of corresponding RunSets
    :return: None
    """
    for run_set_id in run_set_ids:
        calculate_avg_run_set_results(run_set_id)
        calculate_best_run_set_results(run_set_id)


def process_single_run(
    param_set: ParamSet,
    pmax: float,
    run_num: int,
    test_suite_id=None,
    run_set_id=None,
):
    run = Run(number=run_num)
    init_pop = InitPopulation.get(
        run_number=run_num,
        init=param_set.init,
        L=param_set.L,
        N=param_set.N,
        dim_n=param_set.func_case.func_param.dim_n,
        accuracy_decimals=param_set.func_case.func_param.accuracy_decimals,
    )
    run.init_population = init_pop.id
    init_pop_seed = init_pop.seed
    # TODO init disrt
    run.init_distr_health = None

    # Helping vars
    coder_info = param_set.encoding
    coder_info['a'] = param_set.func_case.func_param.interval_a
    coder_info['b'] = param_set.func_case.func_param.interval_b
    f_init = mappers.INIT_MAP[param_set.init]
    f_select = mappers.SEL_TYPE_MAP[param_set.sel_type]
    f_estim = get_estimation_function(param_set)
    STEPS_BACK, MAX_NFE, EPS = get_stop_cond_params(param_set)
    N = param_set.N
    L = param_set.L

    logger.info('Run taken into work', extra={
        'data': {
            'param_set_id': param_set.id,
            'run_num': run_num,
            'run_set_id': run_set_id,
            'test_suite_id': test_suite_id,
        }})

    # Initialization
    # pop: population with decimal values
    # pop_encoded: population represented as 1s and 0s
    pop_encoded = f_init(N, L, init_pop_seed)
    pop = decode(pop_encoded, L, coder_info)
    health = f_estim(pop)
    nfe = N
    iter_num = 0
    mean_health_ar = [health.mean()]
    max_health_ar = [health.max()]
    step = 0
    prev_mean_health = health.mean()

    while nfe < MAX_NFE and not step > STEPS_BACK:
        pop_encoded = f_select(pop_encoded, health, N)
        pop_encoded = crossover(pop_encoded, param_set.crossover_pc)
        pop_encoded = mutate(pop_encoded, pmax)
        pop = decode(pop_encoded, L, coder_info)
        health = f_estim(pop)
        nfe += N
        iter_num += 1
        mean_health = health.mean()
        mean_health_ar.append(mean_health)
        max_health_ar.append(health.max())

        if abs(mean_health - prev_mean_health) < EPS:
            step += 1
        else:
            step = 0
        prev_mean_health = mean_health

    # Last values
    last_pop = pop
    last_health = health
    last_pop_encoded = pop_encoded

    run.is_succ = nfe < MAX_NFE
    run.NFE = nfe
    run.iter_num = iter_num

    if run.is_succ:
        # Helping vars
        optimal_val = np.array([param_set.func_case.extremums[0]])  # optimal dec X for the function
        optimal_encoded = encode(optimal_val, L, coder_info)  # optimal bin/gray X for this function
        f_opt = f_estim(optimal_val)[0]  # value of function in extremum
        avg = last_health.mean()  # average value of health
        maxp = last_health.max()
        best_index = last_health.argmax()
        maxp_encoded = last_pop_encoded[best_index]

        run.avg_health = avg
        run.max_health = last_health.max()
        run.std_health = last_health.std()

        run.avg_health_deviation_to_opt_abs = abs(avg - f_opt)
        run.avg_health_deviation_to_opt_rel = abs((avg - f_opt) / f_opt)
        run.best_health_deviation_to_opt_abs = abs(maxp - f_opt)
        run.best_health_deviation_to_opt_rel = abs((maxp - f_opt) / f_opt)

        run.eucl_d_to_extremum = abs(maxp - f_opt)
        run.hamm_d_to_extremum = hamming_distance_between(maxp_encoded, optimal_encoded)

        run.best_ind = last_pop[best_index]
        run.best_ind_n = len(np.argwhere(last_pop == last_pop[best_index]))

        #
        run.final_distr_hamm = target_hamming_distribution(optimal_encoded, pop_encoded)
        run.final_distr_health = None
        run.final_distr_pairwise = pairwise_hamming_distribution(pop_encoded)

        run.max_avg_health_arr = max_health_ar
        run.avg_avg_health_arr = mean_health_ar

        if test_suite_id is not None:
            run.test_suite = test_suite_id
        else:
            run.run_set = run_set_id

    run.save()
    logger.info('Run completed successfully', extra={'data': {'run_id': run.id}})

    return run


TASK_REGISTRY = {
    TaskType.CREATE_EXP_SUITE: create_exp_suite,
    TaskType.PROCESS_TEST_SUITE: process_test_suite,
    TaskType.FINALIZE_TEST_SUITE: finalize_test_suites,
    TaskType.PROCESS_RUN_SET: process_run_set,
    TaskType.FINALIZE_RUN_SET: finalize_run_set,
}
