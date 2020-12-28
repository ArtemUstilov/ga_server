import peewee
from playhouse.postgres_ext import JSONField, ArrayField

import task_2.helpers.constants as constants
from task_2.helpers.db_utils import BaseModel


class Log(BaseModel):
    level = peewee.CharField(
        choices=[
            ('INFO', 'INFO'), ('WARNING', 'WARNING'), ('ERROR', 'ERROR'), ('EXCEPTION', 'EXCEPTION')
        ],
        max_length=15,
        null=False
    )
    name = peewee.CharField(max_length=100, null=False)
    process_name = peewee.CharField(max_length=50, null=False, default='unknown')
    message = peewee.CharField(null=False)
    extra = JSONField(null=False, default=dict)

    def __str__(self):
        return f'Log: {self.created.isoformat()} - {self.level} - {self.message}'


class Task(BaseModel):
    action = peewee.CharField(
        max_length=50,
        null=False,
        choices=constants.TASKS,
    )
    kwargs = JSONField(
        null=False,
        default=dict
    )
    pending_tasks = JSONField(
        null=False,
        default=list
    )
    taken = peewee.BooleanField(
        null=False,
        default=False,
    )
    completed = peewee.BooleanField(
        null=False,
        default=False,
    )


class Function(BaseModel):
    alias = peewee.CharField(unique=True, max_length=50, choices=constants.ESTIMS)

    def __str__(self):
        return f'Function: {self.alias}'


class FuncParam(BaseModel):
    dim_n = peewee.SmallIntegerField(null=False)
    interval_a = peewee.DoubleField(null=False)
    interval_b = peewee.DoubleField(null=False)
    accuracy_decimals = peewee.SmallIntegerField(null=False)

    def __str__(self):
        return (
            f'FuncParam: n={self.dim_n} [{self.interval_a}; {self.interval_b}] '
            f'q=10^-{self.accuracy_decimals}'
        )


class FuncCase(BaseModel):
    extremums = JSONField(null=False, default=list)

    func_param = peewee.ForeignKeyField(
        FuncParam,
        null=False,
        on_delete='RESTRICT',
        lazy_load=True,
    )
    function = peewee.ForeignKeyField(
        Function,
        null=False,
        on_delete='RESTRICT',
        lazy_load=True,
    )


class InitPopulation(BaseModel):
    run_number = peewee.SmallIntegerField(null=False)
    init = peewee.CharField(
        null=False,
        choices=constants.INITS,
    )
    L = peewee.IntegerField(
        null=False
    )
    N = peewee.IntegerField(
        null=False
    )
    seed = peewee.IntegerField(
        null=False,
        unique=True,
    )

    dim_n = peewee.SmallIntegerField(null=False)
    accuracy_decimals = peewee.SmallIntegerField(null=False)

    init_distr_hamm = ArrayField(peewee.IntegerField, null=True)


class ParamSet(BaseModel):
    """
    De facto, Experiments which we are running
    """

    encoding = JSONField(
        null=False,
        default=dict,
    )
    init = peewee.CharField(
        null=False,
        choices=constants.INITS,
    )
    sel_type = peewee.CharField(
        null=False,
        choices=constants.SEL_TYPES,
    )
    L = peewee.IntegerField(
        null=False
    )
    N = peewee.IntegerField(
        null=False
    )
    stop_cond = JSONField(
        null=False,
        default=dict
    )
    num_runsets = peewee.IntegerField(
        null=False
    )
    num_runs = peewee.IntegerField(
        null=False
    )
    crossover_pc = peewee.DoubleField(
        null=False
    )

    result_pmax = peewee.DoubleField(
        null=True
    )
    action_log = JSONField(
        null=False,
        default=list
    )

    func_case = peewee.ForeignKeyField(
        FuncCase,
        null=False,
        on_delete='RESTRICT',
        lazy_load=True,
        backref='param_sets'
    )


class ExperimentsSuite(BaseModel):
    p_start = peewee.DoubleField(
        null=False,
        help_text="We sart with this value out ParamSet"
    )
    final_succ_n = peewee.IntegerField(
        null=True
    )
    final_succ_pmax = peewee.DoubleField(
        null=True
    )

    param_set = peewee.ForeignKeyField(
        ParamSet,
        null=False,
        on_delete='RESTRICT',
        lazy_load=True,
        backref='exp_suites'
    )


class TestSuite(BaseModel):
    init_pmax = peewee.DoubleField(
        help_text='Pmax value with which the test suite was started',
        null=False
    )
    is_approved = peewee.BooleanField(null=True)
    factor = peewee.DoubleField(null=False)
    succ_num = peewee.IntegerField(null=True)
    is_succ = peewee.BooleanField(null=True)

    # Avg fields

    avg_NFE = peewee.DoubleField(null=True)
    avg_iter_num = peewee.DoubleField(null=True)

    avg_avg_health = peewee.DoubleField(null=True)
    avg_max_health = peewee.DoubleField(null=True)
    avg_std_health = peewee.DoubleField(null=True)

    avg_avg_health_deviation_to_opt_abs = peewee.DoubleField(null=True)
    avg_best_health_deviation_to_opt_abs = peewee.DoubleField(null=True)
    avg_avg_health_deviation_to_opt_rel = peewee.DoubleField(null=True)
    avg_best_health_deviation_to_opt_rel = peewee.DoubleField(null=True)

    avg_eucl_d_to_extremum = peewee.DoubleField(null=True)
    avg_hamm_d_to_extremum = peewee.DoubleField(null=True)

    avg_best_ind = peewee.DoubleField(null=True)
    avg_best_ind_n = peewee.DoubleField(null=True)

    # Best fields

    best_NFE = peewee.IntegerField(null=True)
    best_iter_num = peewee.IntegerField(null=True)

    best_avg_health = peewee.DoubleField(null=True)
    best_max_health = peewee.DoubleField(null=True)
    best_std_health = peewee.DoubleField(null=True)

    best_avg_health_deviation_to_opt_abs = peewee.DoubleField(null=True)
    best_best_health_deviation_to_opt_abs = peewee.DoubleField(null=True)
    best_avg_health_deviation_to_opt_rel = peewee.DoubleField(null=True)
    best_best_health_deviation_to_opt_rel = peewee.DoubleField(null=True)

    best_eucl_d_to_extremum = peewee.DoubleField(null=True)
    best_hamm_d_to_extremum = peewee.IntegerField(null=True)

    best_best_ind = peewee.IntegerField(null=True)
    best_best_ind_n = peewee.IntegerField(null=True)

    exp_suite_before = peewee.ForeignKeyField(
        ExperimentsSuite,
        null=True,
        on_delete='RESTRICT',
        lazy_load=True,
        backref='before_test_suites'
    )
    exp_suite_after = peewee.ForeignKeyField(
        ExperimentsSuite,
        null=True,
        on_delete='RESTRICT',
        lazy_load=True,
        backref='after_test_suites'
    )


class RunSet(BaseModel):
    pmax = peewee.DoubleField(null=False)
    try_number = peewee.SmallIntegerField(
        null=False,
        default=constants.DEFAULT_TRY_NUM,
    )
    succ_num = peewee.IntegerField(null=True)

    # Avg fields

    avg_NFE = peewee.DoubleField(null=True)
    avg_iter_num = peewee.DoubleField(null=True)

    avg_avg_health = peewee.DoubleField(null=True)
    avg_max_health = peewee.DoubleField(null=True)
    avg_std_health = peewee.DoubleField(null=True)

    avg_avg_health_deviation_to_opt_abs = peewee.DoubleField(null=True)
    avg_best_health_deviation_to_opt_abs = peewee.DoubleField(null=True)
    avg_avg_health_deviation_to_opt_rel = peewee.DoubleField(null=True)
    avg_best_health_deviation_to_opt_rel = peewee.DoubleField(null=True)

    avg_eucl_d_to_extremum = peewee.DoubleField(null=True)
    avg_hamm_d_to_extremum = peewee.DoubleField(null=True)

    avg_best_ind = peewee.DoubleField(null=True)
    avg_best_ind_n = peewee.DoubleField(null=True)

    # Best fields

    best_NFE = peewee.IntegerField(null=True)
    best_iter_num = peewee.IntegerField(null=True)

    best_avg_health = peewee.DoubleField(null=True)
    best_max_health = peewee.DoubleField(null=True)
    best_std_health = peewee.DoubleField(null=True)

    best_avg_health_deviation_to_opt_abs = peewee.DoubleField(null=True)
    best_best_health_deviation_to_opt_abs = peewee.DoubleField(null=True)
    best_avg_health_deviation_to_opt_rel = peewee.DoubleField(null=True)
    best_best_health_deviation_to_opt_rel = peewee.DoubleField(null=True)

    best_eucl_d_to_extremum = peewee.DoubleField(null=True)
    best_hamm_d_to_extremum = peewee.IntegerField(null=True)

    best_best_ind = peewee.IntegerField(null=True)
    best_best_ind_n = peewee.IntegerField(null=True)

    exp_suite = peewee.ForeignKeyField(
        ExperimentsSuite,
        null=False,
        on_delete='RESTRICT',
        lazy_load=True,
        backref='run_sets'
    )


class Run(BaseModel):
    number = peewee.SmallIntegerField(null=False)
    is_succ = peewee.BooleanField(null=False)

    init_population = peewee.ForeignKeyField(
        InitPopulation,
        null=False,
        on_delete='RESTRICT',
        lazy_load=True,
    )

    NFE = peewee.IntegerField(null=False)
    iter_num = peewee.IntegerField(null=False)

    avg_health = peewee.DoubleField(null=True)
    max_health = peewee.DoubleField(null=True)
    std_health = peewee.DoubleField(null=True)

    avg_health_deviation_to_opt_abs = peewee.DoubleField(null=True)
    avg_health_deviation_to_opt_rel = peewee.DoubleField(null=True)

    best_health_deviation_to_opt_abs = peewee.DoubleField(null=True)
    best_health_deviation_to_opt_rel = peewee.DoubleField(null=True)

    eucl_d_to_extremum = peewee.DoubleField(null=True)
    hamm_d_to_extremum = peewee.IntegerField(null=True)

    best_ind = peewee.DoubleField(null=True)
    best_ind_n = peewee.IntegerField(null=True)

    init_distr_health = ArrayField(peewee.IntegerField, null=True)

    final_distr_hamm = ArrayField(peewee.IntegerField, null=True)
    final_distr_health = ArrayField(peewee.IntegerField, null=True)
    final_distr_pairwise = ArrayField(peewee.IntegerField, null=True)

    max_avg_health_arr = ArrayField(peewee.DoubleField, null=True)
    avg_avg_health_arr = ArrayField(peewee.DoubleField, null=True)

    run_set = peewee.ForeignKeyField(
        RunSet,
        null=True,
        on_delete='RESTRICT',
        lazy_load=True,
        backref='runs'
    )

    test_suite = peewee.ForeignKeyField(
        TestSuite,
        null=True,
        on_delete='RESTRICT',
        lazy_load=True,
        backref='test_runs'
    )
