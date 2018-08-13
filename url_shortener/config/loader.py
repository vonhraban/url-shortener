import yaml

class ConfigLoader(object):
    @staticmethod
    def load(filename):
        raise NotImplementedError("Not implemented")


class YamlConfigLoader(ConfigLoader):
    @staticmethod
    def load(filename):
        try:
            return yaml.load(open(filename))
        except Exception:
            return None
