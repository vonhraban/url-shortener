class StorageInterface(object):
    """Some description that tells you it's abstract,
    often listing the methods you're expected to supply."""
    def set( self, key, value, ttl):
        raise NotImplementedError("Not implemented")

    def get(self, key):
        raise NotImplementedError("Not implemented")

    def refresh_ttl(self, key, ttl):
        raise NotImplementedError("Not implemented")

