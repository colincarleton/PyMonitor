import os
import logging
import sys
# import pathlib
from logging.handlers import TimedRotatingFileHandler


class LogInfo(object):
    def __init__(self, config):
        config['loglevel'] = 'INFO' if not 'loglevel' in config else config['loglevel']
        config['logdir'] = '/var/log/pymonitor/' if not 'logdir' in config else config['logdir']
        config['logformat'] = 'default' if not 'logformat' in config else config['logformat']
        config['logfile'] = 'monitoring.log'
        try:
            pt = os.path.exists(config['logdir'])
            if not pt:
                pathlib.Path(config['logdir']).mkdir(parents=True, exist_ok=True)
        except FileNotFoundError as ex:
            raise FileNotFoundError('Cannot create log directory: {0}'.format(ex))

        try:
            os.stat(config['logdir'])
        except PermissionError as ex:
            raise PermissionError('Log directory permission denied: {}'.format(ex))

        self.log_level = getattr(logging, config['loglevel'].upper(), None)
        self.format = '%(asctime)s [%(levelname)-5.5s]:  %(message)s'
        self.sformat = '[%(levelname)-5.5s]:  %(message)s'
        if not isinstance(self.log_level, int):
            raise ValueError('Invalid log level: {0}'.format(config['loglevel']))

        self.StreamHandler = logging.StreamHandler(sys.stderr)
        self.StreamHandler.setFormatter(logging.Formatter(self.sformat))
        self.TimedRotatingFileHandler = TimedRotatingFileHandler(
            filename=os.path.join(config['logdir'], config['logfile']),
            backupCount=5,
            when='midnight',
            interval=1)
        self.TimedRotatingFileHandler.setFormatter(logging.Formatter(self.format))
        self.TimedRotatingFileHandler.suffix = '%Y-%m-%d'