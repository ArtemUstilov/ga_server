import logging.config
import os
import time

from task_2.helpers.log import log_config
from task_2.helpers.tasks import pop_task
from task_2.tasks import TASK_REGISTRY

logging.config.dictConfig(log_config)

logger = logging.getLogger(__name__)


def looper():
    # Take one task from DB
    task = pop_task()
    try:
        count = 0
        while task is None:
            count += 1
            if count >= 10:
                logger.info('No tasks. Shutting down')
                return

            logger.info('No tasks. Retry')
            time.sleep(30)
            task = pop_task()

        logger.info('Acknowledged task', extra={'task_id': task.id})

        # Find task implementation
        try:
            task_func = TASK_REGISTRY[task.action]
        except KeyError:
            logger.exception('Invalid task action', exc_info=True)
            return

        # Run task
        try:
            task_func(task, **task.kwargs)
        except Exception:
            logger.exception('Task failed', extra={'task_id': task.id}, exc_info=True)
            return

        # Finish
        task.completed = True
        task.save()
        logger.info('Task completed', extra={'task_id': task.id})
    except (KeyboardInterrupt, InterruptedError):
        task.taken = False
        task.save()
        raise


def main(proc_name):
    os.environ['PROCESS_NAME'] = proc_name
    logger.info('Starting process')
    try:
        while True:
            looper()
    except (KeyboardInterrupt, InterruptedError):
        logger.warning('Shutting down process')
