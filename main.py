import logging

from task.runner import run_parameters

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='./log/processes.log')

logger = logging.getLogger(__name__)


def main():
    inits = ['all_0']
    estims = ['l-hamming_d']
    sel_types = ['rws']
    ls = [10, 20, 40, 60, 80, 100]
    ns = [100, 150, 200]
    algos = ['run_param_set', 'run_param_set_v2']

    logger.info('String up processes')
    run_parameters(inits, estims, sel_types, ls, ns, algos)
    logger.info('Finished')


if __name__ == '__main__':
    main()
