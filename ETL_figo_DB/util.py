from typing import Mapping, Collection


def to_json(obj):
    if hasattr(obj, 'to_json'):
        return obj.to_json()
    elif isinstance(obj, str):
        return obj
    elif isinstance(obj, Mapping):
        return {to_json(k): to_json(v) for k, v in obj.items()}
    elif isinstance(obj, Collection):
        return [to_json(x) for x in obj]
    else:
        return obj
