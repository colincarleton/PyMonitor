import logging
import stat
import os
from hipnotify import Room
from .modules.rabbitmq.main import *


class Capture(object):
    def __init__(self, modules):
        logging.getLogger(__name__)
        self.modules = modules

    def validate_modules(self):
        enabled = [m for m, e in self.modules.items() if self.modules[m] == 'enabled']
        return enabled

    @staticmethod
    def test_rabbitmq(config):
        rabbit = RabbitMQ(config)
        cred = rabbit.test_credentials()
        action = rabbit.load_action()
        return cred, action

    def run_rabbitmq(self, config, action):
        rabbit = RabbitMQ(config)
        data = rabbit.get_queues(action)
        return data


class Alert(object):
    def __init__(self, config):
        self.HIPCHAT_TOKEN = config['hipchat_token']
        self.HIPCHAT_ROOM_ID = config['hipchat_room']
        self.room = Room(self.HIPCHAT_TOKEN, self.HIPCHAT_ROOM_ID)

    def run(self, data):
        try:
            for d in data:
                if d['status'] == 1:
                    continue
                elif d['status'] == 2:
                    self.room.notify(
                        "--------------------------------------------------------------------------------\n"
                        "RabbitMQ Message Queue Filled\n"
                        "--------------------------------------------------------------------------------\n"
                        "Queue: {0}\n"
                        "Environment: {1}\n"
                        "Messages in Queue: {2}\n"
                        "Message Processing Rate: {3}".format(d['queue'], d['env'], d['messages_remaining'], d['process_rate'])
                    )
                    continue
                elif d['status'] == 3:
                    self.room.notify(
                        "--------------------------------------------------------------------------------\n"
                        "RabbitMQ Messages processing slowly\n"
                        "--------------------------------------------------------------------------------\n"
                        "Queue: {0}\n"
                        "Environment: {1}\n"
                        "Messages in Queue: {2}\n"
                        "Message Processing Rate: {3}".format(d['queue'], d['env'], d['messages_remaining'], d['process_rate'])
                    )
                    continue
                elif d['status'] == 4:
                    self.room.notify(
                        "--------------------------------------------------------------------------------\n"
                        "RabbitMQ Health Rule Violation\n"
                        "--------------------------------------------------------------------------------\n"
                        "Reason: Unknown\n"
                        "Queue: {0}\n"
                        "Environment: {1}\n"
                        "Messages in Queue: {2}\n"
                        "Message Processing Rate: {3}".format(d['queue'], d['env'], d['messages_remaining'], d['process_rate'])
                    )
                    continue
        except Exception as ex:
            raise Exception('Error: {}'.format(ex))
