from tinydb import TinyDB, Query, where
from .tools import *


def run_alerts(db, alerts):
    alert = RabbitAlerts().run(db)
    logging.debug(alert)
    alerts.run(alert)


def update_db(data, db, retain=10):
    logging.getLogger(__name__)
    try:
        for d in data:
            timestamp = []
            loc = [loc for loc in db if loc == d['db']]
            tinydb = db[loc[0]]
            store = d['environment'] + '.' + d['table']
            table = tinydb.table(store)
            table.insert(d)
            logging.debug('Saved data to index: {}'.format(store))
            result = table.all()
            for r in result:
                timestamp.append(r['timestamp'])
            timestamp = sorted(timestamp)
            length = len(timestamp) - retain
            if length > 0:
                delete_items = timestamp[0:length]
                logging.debug('Cleaned up {0} values from index: {1}'.format(length, store))
                for item in delete_items:
                    table.remove(where('timestamp') == item)
            else:
                logging.debug('No values to cleanup on index: {}'.format(store))
    except Exception as ex:
        raise Exception('Failure to update database: {}'.format(ex))
    logging.info('Database update(s) complete.')


def run_capture(config, db):
    logging.info('Running Capture')
    capture = Capture(config['modules'])
    capture.validate_modules()
    test, action = capture.test_rabbitmq(config['rabbitmq'])
    data = capture.run_rabbitmq(config['rabbitmq'], action)
    update_db(data, db)

