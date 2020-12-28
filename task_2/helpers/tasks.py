import logging
from typing import Optional

from peewee import fn

from task_2.helpers import constants
from task_2.models import Task

logger = logging.getLogger(__name__)


class TaskType:
    CREATE_EXP_SUITE = constants.CREATE_EXP_SUITE_TASK[0]
    PROCESS_TEST_SUITE = constants.PROCESS_TEST_SUITE_TASK[0]
    FINALIZE_TEST_SUITE = constants.FINALIZE_TEST_SUITE_TASK[0]
    PROCESS_RUN_SET = constants.PROCESS_RUN_SET_TASK[0]
    FINALIZE_RUN_SET = constants.FINALIZE_RUN_SET_TASK[0]


def create_task(action, pending_tasks=None, **kwargs):
    logger.info('Scheduled task', extra={'task_name': action})
    task = Task(action=action, kwargs=kwargs)
    if pending_tasks:
        task.pending_tasks = pending_tasks

    task.save()

    return task


def remove_pending_task(pending_id, target_id):
    try:
        task = Task.get_by_id(target_id)
        task.pending_tasks = list(filter(lambda x: x != pending_id, task.pending_tasks))
        task.save()
    except Exception:
        logger.exception('Could remove pending task', exc_info=True)


def pop_task() -> Optional[Task]:
    subq = (
        Task
        .select(Task.id)
        .where(fn.JSON_ARRAY_LENGTH(Task.pending_tasks) == 0, Task.taken >> False)
        .order_by(Task.id)
        .limit(1)
    )
    query = (
        Task
        .update(taken=True)
        .where(Task.id.in_(subq))
        .returning(Task)
    )

    for task in query.execute():
        return task
