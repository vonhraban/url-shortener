from .adapter import StorageInterface
import etcd


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