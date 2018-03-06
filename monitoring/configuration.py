import pathlib
from .plugins.plugins import PluginManager
from .utils import *
from .exceptions import *
from .logger import LogInfo
from .validators import client_options, schema


class Configuration(object):
    def __init__(self, config):
        with open(config, 'r') as yaml_file:
            config = yaml.load(yaml_file)
        try:
            self.config = {}
            schema.Check(config, client_options.validate()).result()
            log_options = LogInfo(config['logging'])
            logging.root.addHandler(log_options.StreamHandler)
            logging.root.addHandler(log_options.TimedRotatingFileHandler)
            logging.root.setLevel(log_options.log_level)
            logging.info('Configuration loaded. Running Setup...')
            self.data_path = '/var/lib/pymonitor/' if 'data' not in config['path'] else config['path']['data']
            self.plugin_path = '/usr/share/pymonitor/plugins' if 'plugin' not in config['path'] else config['path']['plugin']
        except ConfigurationError as ex:
            raise('Error parsing configuration file: {0}'.format(ex))
        try:
            pt = os.path.exists(self.data_path)
            if not pt:
                pathlib.Path(self.data_path).mkdir(parents=True, exist_ok=True)
            logging.debug('Data Directory: ' + self.data_path)
        except FileNotFoundError as ex:
            raise FileNotFoundError('Cannot create data directory: {0}'.format(ex))

    def plugins(self):
        return 'hi'

    def database(self):
        try:
            gen = {}
            for k, v in self.plugins.items():
                if v == 'enabled':
                    path = os.path.join(self.data_path, (k + '.json'))
                    db = (TinyDB(path, default_table=k))
                    logging.info('Loaded database for module: {}'.format(k))
                    gen.update({k: db})
            return gen
        except Exception as ex:
            raise Exception('Error with TinyDB creation: {}'.format(ex))