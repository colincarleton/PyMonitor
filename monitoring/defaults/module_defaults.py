from voluptuous import *


def module_list():
    return {
        Optional('modulepath'): Any(None, str, unicode),
        Optional('rabbitmq'): Any(None, str, unicode),
        Optional('elastic'): Any(None, str, unicode),
    }