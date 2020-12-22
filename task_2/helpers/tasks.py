import logging
from typing import Optional

from peewee import fn

from task_2.helpers import constants
from task_2.models import Task

logger = logging.getLogger(__name__)


class TaskType:
    CREATE_EXP_SUITE = constants.CREATE_EXP_SUITE_TASK
    PROCESS_TEST_SUITE = constants.PROCESS_TEST_SUITE_TASK
    FINALIZE_TEST_SUITE = constants.FINALIZE_TEST_SUITE_TASK
    PROCESS_RUN_SET = constants.PROCESS_RUN_SET_TASK
    FINALIZE_RUN_SET = constants.FINALIZE_RUN_SET_TASK


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
        .limit(1)
    )
    cursor = (
        Task
        .update(taken=True)
        .where(Task.id.in_(subq))
        .returning(Task)
        .execute()
    )

    if cursor.count == 1:
        return cursor[0]
