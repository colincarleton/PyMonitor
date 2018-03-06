# from voluptuous import *
from .config_defaults import *


def validate():
    config = Schema(
        {
            Optional('path'): path(),
            Optional('logging'): logging(),
            Optional('plugins'): plugins(),
        }
    )
    return config