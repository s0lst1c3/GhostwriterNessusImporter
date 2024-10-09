from datetime import datetime, date
from enum import Enum


def default_encoder(obj):
    if isinstance(obj, Enum):
        return obj.value
    if isinstance(obj, datetime) or isinstance(obj, date):
        return obj.isoformat()
    return str(obj)
