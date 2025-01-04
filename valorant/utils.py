import json

try:
    import msgspec
except ImportError:  # pragma: no cover
    msgspec = None  # type: ignore[assignment]


if msgspec is None:  # noqa: SIM108
    _from_json = json.loads
else:
    _from_json = msgspec.json.decode
