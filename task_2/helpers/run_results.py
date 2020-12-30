from typing import Union, List

import numpy as np

from task_2.models import TestSuite, Run, RunSet


def _calculate_avg(obj: Union[TestSuite, RunSet], runs: List[Run]):
    if not len(runs):
        return obj
    n = len(runs)
    nfe_sum = 0
    iter_num_sum = 0

    avg_health_sum = 0.
    max_health_sum = 0.
    std_health_sum = 0.

    avg_health_deviation_to_opt_abs_sum = 0.
    best_health_deviation_to_opt_abs_sum = 0.
    avg_health_deviation_to_opt_rel_sum = 0.
    best_health_deviation_to_opt_rel_sum = 0.

    eucl_d_to_extremum_sum = 0.
    hamm_d_to_extremum_sum = 0

    best_ind_sum = 0
    best_ind_n_sum = 0

    for run in runs:
        nfe_sum += run.NFE
        iter_num_sum += run.iter_num

        avg_health_sum += run.avg_health
        max_health_sum += run.max_health
        std_health_sum += run.std_health

        avg_health_deviation_to_opt_abs_sum += run.avg_health_deviation_to_opt_abs
        best_health_deviation_to_opt_abs_sum += run.best_health_deviation_to_opt_abs
        avg_health_deviation_to_opt_rel_sum += run.avg_health_deviation_to_opt_rel
        best_health_deviation_to_opt_rel_sum += run.best_health_deviation_to_opt_rel

        eucl_d_to_extremum_sum += run.eucl_d_to_extremum
        hamm_d_to_extremum_sum += run.hamm_d_to_extremum

        best_ind_sum += run.best_ind
        best_ind_n_sum += run.best_ind_n

    obj.succ_num = n
    obj.avg_NFE = nfe_sum / n
    obj.avg_iter_num = iter_num_sum / n

    obj.avg_avg_health = avg_health_sum / n
    obj.avg_max_health = max_health_sum / n
    obj.avg_std_health = std_health_sum / n

    obj.avg_avg_health_deviation_to_opt_abs = avg_health_deviation_to_opt_abs_sum / n
    obj.avg_best_health_deviation_to_opt_abs = best_health_deviation_to_opt_abs_sum / n
    obj.avg_avg_health_deviation_to_opt_rel = avg_health_deviation_to_opt_rel_sum / n
    obj.avg_best_health_deviation_to_opt_rel = best_health_deviation_to_opt_rel_sum / n

    obj.avg_eucl_d_to_extremum = eucl_d_to_extremum_sum / n
    obj.avg_hamm_d_to_extremum = hamm_d_to_extremum_sum / n

    obj.avg_best_ind = best_ind_sum / n
    obj.avg_best_ind_n = best_ind_n_sum / n
    return obj


def _calculate_best(obj: Union[TestSuite, RunSet], runs: List[Run]):
    if not len(runs):
        return obj
    best_nfe = 0
    best_iter_num = 0

    best_avg_health = float('-inf')
    best_max_health = float('-inf')
    best_std_health = float('-inf')

    best_avg_health_deviation_to_opt_abs = float('-inf')
    best_best_health_deviation_to_opt_abs = float('-inf')
    best_avg_health_deviation_to_opt_rel = float('-inf')
    best_best_health_deviation_to_opt_rel = float('-inf')

    best_eucl_d_to_extremum = 0.
    best_hamm_d_to_extremum = 0

    best_best_ind = float('-inf')
    best_best_ind_n = 0

    for run in runs:
        best_nfe = max(best_nfe, run.NFE)
        best_iter_num = max(best_iter_num, run.iter_num)

        best_avg_health = max(best_avg_health, run.avg_health)
        best_max_health = max(best_max_health, run.max_health)
        best_std_health = max(best_std_health, run.std_health)

        best_avg_health_deviation_to_opt_abs = max(
            best_avg_health_deviation_to_opt_abs,
            run.avg_health_deviation_to_opt_abs
        )
        best_best_health_deviation_to_opt_abs = max(
            best_best_health_deviation_to_opt_abs,
            run.best_health_deviation_to_opt_abs
        )
        best_avg_health_deviation_to_opt_rel = max(
            best_avg_health_deviation_to_opt_rel,
            run.avg_health_deviation_to_opt_rel
        )
        best_best_health_deviation_to_opt_rel = max(
            best_best_health_deviation_to_opt_rel,
            run.best_health_deviation_to_opt_rel
        )

        best_eucl_d_to_extremum = max(best_eucl_d_to_extremum, run.eucl_d_to_extremum)
        best_hamm_d_to_extremum = max(best_hamm_d_to_extremum, run.hamm_d_to_extremum)

        best_best_ind = max(best_best_ind, run.best_ind)
        best_best_ind_n = max(best_best_ind_n, run.best_ind_n)

    obj.best_NFE = best_nfe
    obj.best_iter_num = best_iter_num

    obj.best_avg_health = best_avg_health
    obj.best_max_health = best_max_health
    obj.best_std_health = best_std_health

    obj.best_avg_health_deviation_to_opt_abs = best_avg_health_deviation_to_opt_abs
    obj.best_best_health_deviation_to_opt_abs = best_best_health_deviation_to_opt_abs
    obj.best_avg_health_deviation_to_opt_rel = best_avg_health_deviation_to_opt_rel
    obj.best_best_health_deviation_to_opt_rel = best_best_health_deviation_to_opt_rel

    obj.best_eucl_d_to_extremum = best_eucl_d_to_extremum
    obj.best_hamm_d_to_extremum = best_hamm_d_to_extremum

    obj.best_best_ind = best_best_ind
    obj.best_best_ind_n = best_best_ind_n
    return obj


def calculate_avg_test_results(test_suite_id):
    testsuite = TestSuite.get(id=test_suite_id)
    runs = list(Run.filter(test_suite_id=test_suite_id, is_succ=True))

    testsuite = _calculate_avg(testsuite, runs)
    testsuite.save()
    return testsuite


def calculate_avg_run_set_results(run_set_id):
    runset = RunSet.get(id=run_set_id)
    runs = list(Run.filter(run_set_id=run_set_id, is_succ=True))

    runset = _calculate_avg(runset, runs)
    runset.save()
    return runset


def calculate_best_test_results(test_suite_id):
    testsuite = TestSuite.get(id=test_suite_id)
    runs = list(Run.filter(test_suite_id=test_suite_id, is_succ=True))

    testsuite = _calculate_best(testsuite, runs)
    testsuite.save()
    return testsuite


def calculate_best_run_set_results(run_set_id):
    runset = RunSet.get(id=run_set_id)
    runs = list(Run.filter(run_set_id=run_set_id, is_succ=True))

    runset = _calculate_best(runset, runs)
    runset.save()
    return runset


def pairwise_hamming_distribution(population):
    matrix = (population[:, None, :] != population).sum(2)
    np.fill_diagonal(matrix, -1)
    d = np.zeros(population.shape[1], dtype=np.int64)
    for i in range(len(d)):
        d[i] = (matrix == i).sum() / 2

    return d
