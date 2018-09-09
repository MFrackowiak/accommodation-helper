import os
from json import load


def read_config():
    # TODO add argparse
    config_filename = os.environ.get('DH_CONFIG_FILE', 'app.config.json')
    with open(config_filename) as config_file:
        return load(config_file)


class DictWithAttrs(dict):
    def __getattr__(self, item):
        return self.__getitem(item)


application_config = read_config()
