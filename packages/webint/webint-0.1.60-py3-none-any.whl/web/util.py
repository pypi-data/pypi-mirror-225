import datetime
import json
import pathlib

import easyuri


def dump(payload, **kwargs) -> dict | list:
    path = kwargs.pop("path", None)
    output = JSONEncoder(**kwargs).encode(payload)
    if path:
        with pathlib.Path(path).open("w") as fp:
            fp.write(output)
    return output


def load(payload=None, path=None) -> dict | list:
    if path:
        with pathlib.Path(path).open("r") as fp:
            return json.load(fp)
    elif payload:
        return json.loads(payload)
    raise RuntimeError("must provide payload or path")


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, easyuri.URI):
            return str(obj)
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return {
                "datetime": obj.in_tz("utc").isoformat(),
                "timezone": obj.timezone.name,
            }
        return json.JSONEncoder.default(self, obj)
