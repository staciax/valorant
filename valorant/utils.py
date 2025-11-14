import json
import os
from pathlib import Path

try:
    import msgspec
except ImportError:  # pragma: no cover
    msgspec = None


_from_json = json.loads if msgspec is None else msgspec.json.decode

IS_PYTEST = os.environ.get('PYTEST_VERSION') is not None


def is_running_in_pytest() -> bool:
    return IS_PYTEST


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
    cache_dir = Path(cache_path)

    cache_dir.mkdir(parents=True, exist_ok=True)

    gitignore_path = cache_dir / '.gitignore'
    if not gitignore_path.exists():
        gitignore_content = '# Ignore all files in this cache directory\n*'

        gitignore_path.write_text(gitignore_content.strip() + '\n')

    return cache_dir
