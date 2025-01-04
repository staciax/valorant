import json

try:
    import msgspec  # type: ignore[import-not-found]
except ImportError:  # pragma: no cover
    msgspec = None


if msgspec is None:  # noqa: SIM108
    _from_json = json.loads
else:
    _from_json = msgspec.json.decode
