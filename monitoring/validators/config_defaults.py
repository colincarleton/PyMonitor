from voluptuous import *


def path():
    return {
        Optional('data', default='/var/lib/pymonitor'): Any(None, str, unicode),
        Optional('plugin', default='/usr/share/pymonitor/modules'): Any(None, str, unicode),
    }


def logging():
    return {
        Optional('loglevel', default='INFO'): Any(None, 'NOTSET', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL', All(Coerce(int), Any(0, 10, 20, 30, 40, 50))),
        Optional('logdir', default='/var/log/pymonitor/'): Any(None, str, unicode),
        Optional('blacklist', default=['elasticsearch', 'urllib3']): Any(None, list),
    }


def plugins():
    return {
        Optional('rabbitmq', default='disabled'): Any(None, 'enabled', 'disabled'),
    }