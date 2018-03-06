from .utils import *
from .exceptions import *
from .validators.schema import SchemaCheck
from .validators import client_options
from .logger import LogInfo


def test_config(yaml_file):
    config = get_yaml(yaml_file)
    return SchemaCheck(config, client_options.validate(), 'Client Configuration').result()


def process_config(yaml_file):
    try:
        config = test_config(yaml_file)
        set_logging(config['logging'])
        logger = logging.getLogger(__name__)
        EnsureTree(config['client'])
        logger.info('Configuration loaded. Running Setup...')
        # alerts = set_alerts(config['alerts'])
        # db = connect_db(config['modules'], config['client'])
        # gen = next(db)
    except ConfigurationError as ex:
        raise ConfigurationError('Unable to load config file: {}'.format(ex))
    return config


def set_logging(log_settings):
    log_options = LogInfo(log_settings)
    logging.root.addHandler(log_options.StreamHandler)
    logging.root.addHandler(log_options.TimedRotatingFileHandler)
    logging.root.setLevel(log_options.log_level)


def run_setup(config):
    logging.debug('test!')


def set_alerts(alert_settings):
    alerts = Alert(alert_settings)
    return alerts


def set_storage(storage_settings):
    storage = Storage(storage_settings).config()
    return storage


def connect_db(modules, datapath):
    try:
        logger = logging.getLogger(__name__)
        gen = {}
        if datapath['storage_type'] == 'default':
            for k, v in modules.items():
                path = os.path.join(datapath['datapath'], (k + '.json'))
                db = (TinyDB(path, default_table=k))
                logger.info('Loaded database for module: {}'.format(k))
                gen.update({k: db})
        yield gen
    except Exception as ex:
        raise Exception('Error with TinyDB creation: {}'.format(ex))


