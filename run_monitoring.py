from monitoring.cli import *


if __name__ == '__main__':
    try:
        config, db, alerts = setup()
        run(config, db, alerts)
    except Exception as ex:
        if 'ASCII' in str(ex):
            print('{0}'.format(ex))
        else:
            import sys
            print('{0}'.format(ex))
            sys.exit(1)
