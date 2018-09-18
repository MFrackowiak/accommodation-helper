import os
from json import load


class DictWithAttrs(dict):
    def __getattr__(self, item):
        return self.__getitem__(item)

    @classmethod
    def from_dict(cls, d):
        if isinstance(d, dict):
            return cls(**{
                key: cls.from_dict(value)
                for key, value in d.items()
            })
        elif isinstance(d, (tuple, list)):
            return [cls.from_dict(value) for value in d]
        else:
            return d


def read_config():
    # TODO add argparse
    config_filename = os.environ.get('DH_CONFIG_FILE', 'app.config.json')
    with open(config_filename) as config_file:
        config_dict = load(config_file)
    return DictWithAttrs.from_dict(config_dict)


application_config = read_config()
