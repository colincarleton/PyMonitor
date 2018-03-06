import logging


class Check(object):
    def __init__(self, config, schema):
        self.logger = logging.getLogger('monitoring.validators.SchemaCheck')
        # Set the Schema for validation...
        self.logger.info('Schema: {0}'.format(schema))
        self.logger.info('config: {0}'.format(config))
        self.config = config
        self.schema = schema

    def result(self):
        try:
            self.logger.error("Validating Configuration File...")
            return self.schema(self.config)
        except Exception as ex:
            self.logger.error("Failed: {}".format(ex))
            raise Exception('Check configuration file: {}'.format(ex))