import json
import os

try:
    import msgspec
except ImportError:  # pragma: no cover
    msgspec = None


_from_json = json.loads if msgspec is None else msgspec.json.decode


def is_running_in_pytest() -> bool:
    return 'VALORANT_PYTEST_CURRENT_TEST' in os.environ
