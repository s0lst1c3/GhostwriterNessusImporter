from configparser import ConfigParser, ExtendedInterpolation
from lib.utils.json import default_encoder
from operator import attrgetter
import copy
import json


def key_not_exception(key, exceptions):
    return exceptions != "*" and not key in exceptions


def key_undefined(key, baseline):
    return key not in baseline


def get_next_exceptions(exceptions, key):
    if exceptions == "*":
        return "*"
    return exceptions.get(key, {})


class Namespace:

    # constructor
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def clear(self):
        self.__dict__ = {}

    def reset(self, **kwargs):
        self.clear()
        self.update(**kwargs)

    def items(self):
        return self.__dict__.items()

    def update(self, **kwargs):
        self.__dict__.update(kwargs)

    @staticmethod
    def from_ini_file(init_file, extended_interpolation=False):
        if extended_interpolation:
            ini = ConfigParser(interpolation=ExtendedInterpolation())
        else:
            ini = ConfigParser()
        ini.read(init_file)
        obj = {section: dict(ini.items(section)) for section in ini.sections()}
        return Namespace.from_dict(obj)

    @staticmethod
    def from_json_file(json_file):
        with open(json_file) as f:
            return Namespace.from_json(f.read())

    def to_json_file(self):
        pass

    @classmethod
    def from_json(cls, my_json):
        return json.loads(my_json, object_hook=cls._from_dict_helper)

    def to_json(self):
        return json.dumps(
            self, default=Namespace._to_dict_helper, sort_keys=True, indent=4
        )

    @staticmethod
    def _to_dict_helper(obj):

        try:
            my_dict = obj.__dict__
        except AttributeError:
            return obj

        return my_dict

    # @staticmethod
    @classmethod
    def from_dict(cls, my_dict):
        return cls.from_json(json.dumps(my_dict, default=default_encoder))

    @classmethod
    def _from_dict_helper(cls, my_dict):
        return cls(**my_dict)

    def to_dict(self, filter=[]):
        my_dict = json.loads(str(self))
        if filter:
            return {k: v for k, v in my_dict.items() if k in filter}
        return my_dict

    def get(self, attr, default=None):
        try:
            value = attrgetter(attr)(self)
        except AttributeError:
            value = default
        return value

    def set(self, attr, value):
        if type(value) == dict:
            value = Namespace.from_dict(value)
        return setattr(self, attr, value)

    def to_new(self, **kwargs):
        new_ns = copy.deepcopy(self)
        for key, value in kwargs.items():
            setattr(new_ns, key, value)
        return new_ns

    @staticmethod
    def _baseline_helper(my_dict, baseline_dict, path=[], exceptions={}):

        for key in my_dict:
            if key_not_exception(key, exceptions) and key_undefined(key, baseline_dict):
                err_path = ".".join(path + [key])
                raise ValueError(
                    f'[!] Invalid parameter found in settings file: key "{err_path}"'
                )
        traversal_targets = []
        self_copies = []
        for key, value in baseline_dict.items():
            if key not in my_dict:
                # input(f"key is {key}")
                if isinstance(value, dict):
                    my_dict[key] = copy.deepcopy(value)
                else:
                    my_dict[key] = copy.deepcopy(value)
            else:
                if isinstance(value, dict):
                    traversal_targets.append(key)
                else:
                    my_dict[key] = copy.deepcopy(my_dict[key])
        for key in traversal_targets:
            value = baseline_dict[key]
            Namespace._baseline_helper(
                my_dict[key],
                baseline_dict[key],
                path + [key],
                exceptions=get_next_exceptions(exceptions, key),
            )
            my_dict[key] = copy.deepcopy(my_dict[key])

    def baseline(self, baseline_ns, exceptions={}):
        my_dict = self.to_dict()
        baseline_dict = baseline_ns.to_dict()
        self._baseline_helper(my_dict, baseline_dict, exceptions=exceptions)
        for key in my_dict:
            if isinstance(my_dict[key], dict):
                my_dict[key] = Namespace.from_dict(my_dict[key])
        self.reset(**my_dict)
        # baselined_ns = Namespace.from_dict(my_dict)
        # return baselined_ns

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.to_json()
