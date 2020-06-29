import logging
import subprocess


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='/tmp/pycharm_project_18/log/sys.log')

logger = logging.getLogger('cron')

result = subprocess.run(['/opt/vc/bin/vcgencmd', 'measure_temp'], stdout=subprocess.PIPE)
decoded = result.stdout.decode('UTF-8').replace('\n', '')

logger.info(f'System temp: {decoded}')
