from .configuration import *


def setup():
    config = Configuration("config.yml")
    test = config.plugins()
    logging.info(test)
    db = config.database()
    logging.info("Configuration Complete.")
    return config, db


def run(config, db):
    logging.info("Running...")
    timer = 0
    while True:
        run_capture(config, db)
        # Timer to limit alert frequency, bad way to do this, fix later
        if timer == 10:
            logging.info('Running Alerts')
            run_alerts(db, alerts)
            timer = 0
        else:
            timer = timer + 1
        time.sleep(60)
