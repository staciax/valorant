import json
import os

try:
    import msgspec
except ImportError:  # pragma: no cover
    msgspec = None


if msgspec is None:  # pragma: no cover  # noqa: SIM108
    _from_json = json.loads
else:
    _from_json = msgspec.json.decode  # pragma: no cover


def is_running_in_pytest() -> bool:
    return 'VALORANT_PYTEST_CURRENT_TEST' in os.environ
