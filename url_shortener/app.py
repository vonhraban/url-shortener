import falcon
import json
import os
from url_shortener.config.loader import YamlConfigLoader
from url_shortener.storage.etcd_adapter import EtcdAdapter
from url_shortener.generator.name_generator import NameGenerator

try:
    CONFIG_FILE = os.environ["CONFIG_FILE"]
except KeyError:
    raise Exception('CONFIG_VALUE EV is not set')


class CacheResource(object):

    def __init__(self, store, name_generator):
        self._store = store
        self._name_generator = name_generator

    def on_get(self, req, resp, name):
        url = self._store.get(name)
        if url is not None:
            resp.status = falcon.HTTP_301
            resp.content_type = "application/json"
            resp.body = (
                '{"moved":"' + url + '"}')
        else:
            resp.status = falcon.HTTP_404
            resp.content_type = "application/json"
            resp.body = (
                '{"error":"url not found"}')

    def on_post(self, req, resp, name):
        doc = json.load(req.stream)
        name = self._name_generator.generate()
        self._store.set(name, doc["url"])
        resp.status = falcon.HTTP_201
        resp.content_type = "application/json"
        resp.body = (
            '{"key":"' + str(name) + '"}')


config = YamlConfigLoader.load(CONFIG_FILE)
if config is None:
    raise Exception("Config can not be loaded")

name_generator = NameGenerator(config)

store = EtcdAdapter(config['etcd_connection']['host'], config['etcd_connection']['port'])


app = falcon.API()
app.add_route('/{name}', CacheResource(store, name_generator))
