import datetime
import json
import logging
import math
import uuid
from decimal import Decimal

import dateutil

try:
    import numpy as np
except ImportError:
    np = None
try:
    import pandas as pd
except ImportError:
    pd = None

_NUMPY_TYPE_MAP = {
    "float": float,
    "float32": float,
    "float64": float,
    "int": int,
    "int32": int,
    "int64": int,
    "bool_": bool,
}

logger = logging.getLogger(__name__)


class EventEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, uuid.UUID):
            return str(obj)
        elif isinstance(obj, datetime.datetime):
            return datetime_isoformat(obj)
        elif type(obj) in _NUMPY_TYPE_MAP.keys():
            new_type = _NUMPY_TYPE_MAP[type(obj)]
            return new_type(obj)
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


def datetime_isoformat(dt: datetime.datetime) -> str:
    iso_str = dt.isoformat()
    if dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None:
        # check if datetime is naive
        # https://docs.python.org/3/library/datetime.html#determining-if-an-object-is-aware-or-naive
        return f"{iso_str}Z"

    return iso_str


def serialize_datetime_like(value):
    error_msg = "Tried to serialize {} as datetime, but not in valid ISOformat".format(value)
    if isinstance(value, datetime.datetime):
        return datetime_isoformat(value)
    elif isinstance(value, str):
        try:
            dateutil.parser.parse(value)
            return value
        except ValueError:
            # Re-raise the exception
            raise ValueError(error_msg)

    raise ValueError(error_msg)


def serializable_value(value):  # noqa: C901
    if value is None:
        return None
    if isinstance(value, str):
        return value
    if isinstance(value, uuid.UUID):
        return str(value)
    if isinstance(value, datetime.datetime):
        return datetime_isoformat(value)
    if np is not None and isinstance(value, np.ndarray):
        return list_encoder(value.tolist())
    if isinstance(value, list) or isinstance(value, tuple):
        return list_encoder(value)
    if isinstance(value, dict):
        return dict_encoder(value)
    if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
        return None
    if pd is not None and isinstance(value, pd.Series):
        return list_encoder(value.to_list())
    if pd is not None and isinstance(value, pd.DataFrame):
        return list_encoder(value.to_dict("records"))
    if isinstance(value, Decimal):
        return float(value)
    if math.isnan(value):
        return None
    if type(value).__name__ in _NUMPY_TYPE_MAP.keys():
        new_type = _NUMPY_TYPE_MAP[type(value).__name__]
        return new_type(value)

    if (
        not isinstance(value, str)
        and not isinstance(value, int)
        and not isinstance(value, bool)
        and not isinstance(value, float)
    ):
        logger.warn("%s of type %s is not serializable", value, type(value))

    return value


def list_encoder(li: list) -> list:
    serializable = list(li)
    for i in range(len(li)):
        value = li[i]
        serializable[i] = serializable_value(value)
    return serializable


def serializable_key(key):
    if key is None:
        return "None"
    if isinstance(key, uuid.UUID):
        return str(key)
    return key


def dict_encoder(d: dict) -> dict:
    serializable = {}
    for key, value in d.items():
        serializable[serializable_key(key)] = serializable_value(value)
    return serializable
