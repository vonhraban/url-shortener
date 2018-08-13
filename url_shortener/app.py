import falcon
import json
import os
import base64
import etcd
from url_shortener.config.loader import YamlConfigLoader

try:
    CONFIG_FILE = os.environ["CONFIG_FILE"]
except KeyError:
    raise Exception('CONFIG_VALUE EV is not set')


class StorageInterface(object):
    """Some description that tells you it's abstract,
    often listing the methods you're expected to supply."""
    def set( self, key, value, ttl):
        raise NotImplementedError("Not implemented")

    def get(self, key):
        raise NotImplementedError("Not implemented")

    def refresh_ttl(self, key, ttl):
        raise NotImplementedError("Not implemented")


class EtcdAdapter(StorageInterface):
    def __init__(self, host, port):
        self.client = etcd.Client(host=host, port=port, allow_redirect=False)

    def set( self, key, value, ttl=300):
        self.client.write(key, value, ttl)

    def get(self, key):
        try:
            return self.client.read(key).value
        except etcd.EtcdKeyNotFound:
            return None

    def refresh_ttl(self, key, ttl):
        self.client.refresh(key, ttl)


class NameGenerator(object):

    @staticmethod
    def generate():
        return base64.urlsafe_b64encode(os.urandom(config['name_generation']['number_of_bytes'])).decode('ascii')


class CacheResource(object):

    def __init__(self, store):
        self._store = store

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
        name = NameGenerator.generate()
        self._store.set(name, doc["url"])
        resp.status = falcon.HTTP_201
        resp.content_type = "application/json"
        resp.body = (
            '{"key":"' + str(name) + '"}')


config = YamlConfigLoader.load(CONFIG_FILE)
if config is None:
    raise Exception("Config can not be loaded")


store = EtcdAdapter(config['etcd_connection']['host'], config['etcd_connection']['port'])


app = falcon.API()
app.add_route('/{name}', CacheResource(store))
