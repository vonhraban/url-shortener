import base64
import os


class NameGenerator(object):

    def __init__(self, config):
        self._config = config

    def generate(self):
        return base64.urlsafe_b64encode(os.urandom(self._config['name_generation']['number_of_bytes'])).decode('ascii')
