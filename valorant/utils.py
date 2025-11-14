import json
import os
import sys

try:
    import msgspec
except ImportError:  # pragma: no cover
    msgspec = None


_from_json = json.loads if msgspec is None else msgspec.json.decode

IS_PYTEST = os.environ.get('PYTEST_CURRENT_TEST') is not None


def is_running_in_pytest() -> bool:
    return True
