from task_2 import models as m
from task_2.helpers.db_utils import database


def drop_tables(*args):
    if not args:
        args = [
            m.Log,
            m.Task,
            m.Function,
            m.FuncParam,
            m.FuncCase,
            m.InitPopulation,
            m.ParamSet,
            m.ExperimentsSuite,
            m.TestSuite,
            m.RunSet,
            m.Run
        ]
    database.drop_tables(args)


def create_tables(*args):
    if not args:
        args = [
            m.Log,
            m.Task,
            m.Function,
            m.FuncParam,
            m.FuncCase,
            m.InitPopulation,
            m.ParamSet,
            m.ExperimentsSuite,
            m.TestSuite,
            m.RunSet,
            m.Run
        ]
    database.create_tables(args)
