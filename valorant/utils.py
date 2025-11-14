import json
import os
from pathlib import Path

try:
    import msgspec
except ImportError:  # pragma: no cover
    msgspec = None


_from_json = json.loads if msgspec is None else msgspec.json.decode


# pytest detection

IS_PYTEST = os.environ.get('PYTEST_VERSION') is not None


def is_running_in_pytest() -> bool:
    return IS_PYTEST


# cache folder path

DEFAULT_CACHE_PATH = Path('./.valorant_cache')


def create_cache_folder(cache_path: str | Path = DEFAULT_CACHE_PATH) -> Path:
    """
    Create a cache folder with .gitignore to exclude it from version control.

    Parameters
    ----------
    cache_path : str | Path
        Path to the cache folder. Defaults to './.valorant_cache'

    Returns
    -------
    Path
        The created cache folder path
    """
    if isinstance(cache_path, str):
        cache_path = Path(cache_path)

    cache_path.mkdir(parents=True, exist_ok=True)

    gitignore_path = cache_path / '.gitignore'
    if not gitignore_path.exists():
        gitignore_content = '# Ignore all files in this cache directory\n*'
        gitignore_path.write_text(gitignore_content + '\n')

    return cache_path
