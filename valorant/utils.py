# mypy: disable-error-code="assignment, import-not-found"

import json

try:
    import msgspec
except ImportError:  # pragma: no cover
    msgspec = None


if msgspec is None:  # pragma: no cover  # noqa: SIM108
    _from_json = json.loads
else:
    _from_json = msgspec.json.decode
