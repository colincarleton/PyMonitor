from voluptuous import *
from ..defaults import client_defaults, module_defaults

def validate():
    config = Schema(
        {
            Optional('client'): client_defaults.client(),
            Optional('logging'): client_defaults.client_logger(),
            Optional('modules'): module_defaults.module_list(),
            Optional('rabbitmq'): module_defaults.module_rabbitmq(),
            Optional('alerts'): module_defaults.module_rabbitmq(),
        }
    )
    return config