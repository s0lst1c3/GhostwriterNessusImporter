import inspect
from varname import argname


from typing import (
    TYPE_CHECKING,
    AbstractSet,
    Any,
    Callable,
    Collection,
    Dict,
    Generator,
    Iterable,
    Iterator,
    List,
    Mapping,
    Optional,
    Set,
    Tuple,
    Type,
    TypeVar,
    Union,
)

KeyType = TypeVar("KeyType")

from pathlib import Path


def get_caller_frame(depth=1):
    frame = inspect.currentframe()
    for _ in range(depth):
        frame = frame.f_back
    return frame


def get_caller_lineno(depth=1):
    return get_caller_frame(depth).f_lineno


def get_caller_name(depth=1):
    return str(get_caller_frame(depth=depth).f_code.co_qualname)


def get_caller_filename(depth=1):
    return Path(get_caller_frame(depth).f_code.co_filename).resolve()


def deep_update(
    mapping: Dict[KeyType, Any],
    *updating_mappings: Dict[KeyType, Any],
    extend_lists=False,
) -> Dict[KeyType, Any]:
    updated_mapping = mapping.copy()
    for updating_mapping in updating_mappings:
        for k, v in updating_mapping.items():
            if (
                k in updated_mapping
                and isinstance(updated_mapping[k], dict)
                and isinstance(v, dict)
            ):
                updated_mapping[k] = deep_update(
                    updated_mapping[k], v, extend_lists=extend_lists
                )
            elif (
                extend_lists
                and k in updated_mapping
                and isinstance(updated_mapping[k], list)
                and isinstance(v, list)
            ):
                updated_mapping[k].extend(v)
            else:
                updated_mapping[k] = v
    return updated_mapping


class classproperty:

    def __init__(self, fget):
        self.fget = fget

    def __get__(self, obj, owner):
        return self.fget(owner)


def ensure_list(val):
    if isinstance(val, list):
        return val
    return [val]


def select_to_list(*args, default=[], empty_is_falsey=True):

    return ensure_list(
        select_value(*args, default=default, empty_is_falsey=empty_is_falsey)
    )


def select_value(*args, default=None, empty_is_falsey=True):
    for arg in args:
        if arg and empty_is_falsey or arg is not None:
            return arg
    return default


def set_if_unset(obj, attr, value):
    if not hasattr(obj, attr):
        setattr(obj, attr, value)


def select_value_no_default(*args):

    for arg in args:
        if arg:
            return arg
    missing_params = ", ".join([argname(f"args[{i}]") for i in range(len(args))])
    raise ValueError(f"At least one parameter must be provided: {missing_params}")
