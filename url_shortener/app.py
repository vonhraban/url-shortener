import falcon
import json
import os
from url_shortener.config.loader import YamlConfigLoader
from url_shortener.storage.etcd_adapter import EtcdAdapter
from url_shortener.generator.name_generator import NameGenerator

try:
    CONFIG_FILE = os.environ['CONFIG_FILE']
except KeyError:
    raise Exception('CONFIG_VALUE EV is not set')


class CacheResource:

    def __init__(self, store, name_generator):
        self._store = store
        self._name_generator = name_generator

    def on_get(self, req, resp, name):
        resp.content_type = 'application/json'

        url = self._store.get(name)
        if url is not None:
            resp.status = falcon.HTTP_301
            resp.body = (
                '{"moved":"' + url + '"}')
            return

        resp.status = falcon.HTTP_404
        resp.content_type = 'application/json'

    def on_post(self, req, resp, name):
        resp.content_type = 'application/json'

        try:
            body = json.load(req.stream)
        except json.decoder.JSONDecodeError:
            resp.status = falcon.HTTP_400
            resp.body = (
                '{"error":"Invalid JSON provided"}')
            return

        if 'url' not in body:
            resp.status = falcon.HTTP_400
            resp.body = (
                '{"error":"`url` parameter is required"}')
            return

        name = self._name_generator.generate()
        self._store.set(name, body["url"])
        resp.status = falcon.HTTP_201
        resp.body = (
            '{"key":"' + str(name) + '"}')


config = YamlConfigLoader.load(CONFIG_FILE)
if config is None:
    raise Exception('Config can not be loaded')

name_generator = NameGenerator(config)
store = EtcdAdapter(config['etcd_connection']['host'], config['etcd_connection']['port'])


def init():
    app = falcon.API()
    app.add_route('/{name}', CacheResource(store, name_generator))
    return app


app = init()
