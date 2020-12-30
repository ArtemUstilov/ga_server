import logging
import os
from datetime import datetime


class LogDbHandler(logging.Handler):

    def handle(self, record: logging.LogRecord) -> None:
        from task_2.models import Log

        log = Log(
            level=record.levelname,
            name=record.name,
            process_name=os.environ.get('PROCESS_NAME'),
            created=datetime.fromtimestamp(record.created),
            message=record.msg,
            extra={
                'raw': str(record.__dict__),
                'data': record.__dict__.get('data', {})
            }
        )

        log.save()
        print(log)


log_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'db_handler': {
            'class': 'task_2.helpers.log.LogDbHandler',
            'level': 'INFO'
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['db_handler'],
    }
}
