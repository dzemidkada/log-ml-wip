import datetime
import hashlib
import os

import yaml


class Config:
    """Basic utility for working with .yaml configs.

    May be used as a base class for more sofisticated configs,
    in case some custom validations are required.
    """

    def __init__(self, path=None):
        if path is None:
            return
        self.path = path
        with open(self.path, 'r') as stream:
            self.cfg = yaml.safe_load(stream)

    def __get_item_nested(self, key):
        if not isinstance(key, str):
            if not isinstance(key, list):
                key = [key]
            res = self.cfg
            for item in key:
                res = res[item]
            return res
        return self.cfg[key]

    def __getitem__(self, key):
        try:
            return self.__get_item_nested(key)
        except KeyError:
            return None

    def __contains__(self, key):
        try:
            return self.__get_item_nested(key) is not None
        except KeyError:
            return False

    @property
    def postfix(self):
        return "{}.{}".format(self.cfg[self.EXPERIMENT_NAME],
                              hashlib.md5(str(self.cfg).encode('utf-8')).hexdigest())

    @property
    def date_postfix(self):
        return "{}.{}".format(datetime.datetime.now().strftime("%Y%m%d"), self.postfix)

    def save(self, file):
        yaml.dump(self.cfg, file, default_flow_style=False)

    @staticmethod
    def _load(stream):
        c = Config(None)
        c.cfg = yaml.load(stream)
        return c

    def __repr__(self):
        return self.path
