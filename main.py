import logging
import sys

from task.runner import run_parameters
from task.tester import run_tester

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='./log/processes.log')

logger = logging.getLogger(__name__)


def main():
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        limit = 10
        if len(sys.argv) == 3:
            limit = sys.argv[2]
        logger.info('Starting testing')
        run_tester(limit)
        logger.info('Finished testing')
    elif len(sys.argv) > 1 and sys.argv[1] == 'run':
        limit = 10
        if len(sys.argv) == 3:
            limit = sys.argv[2]
        logger.info('Starting up processes')
        run_parameters(limit)
        logger.info('Finished processes')


if __name__ == '__main__':
    main()
