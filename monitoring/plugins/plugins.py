#temp
import pathlib
import os


class PluginManager:
    def __init__(self):
        config['path'] = '/usr/share/pymonitor/plugins' if 'path' not in config else config['path']
        self.path = config['path']
        try:
            pt = os.path.exists(self.path)
            if not pt:
                pathlib.Path(self.path).mkdir(parents=True, exist_ok=True)
        except FileNotFoundError as ex:
            raise FileNotFoundError('Cannot create log directory: {0}'.format(ex))

    def __setstate__(self, data):
        PATH_CACHE = data.get('PATH_CACHE')

    def __getstate__(self):
        return dict(
            PATH_CACHE=PATH_CACHE[self.class_name]
        )

    def list_plugins(self):
        return 'hi'