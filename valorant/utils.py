import json
import os
import shutil
from pathlib import Path
from typing import Final

try:
    import msgspec
except ImportError:  # pragma: no cover
    msgspec = None


__all__ = (
    'create_cache_folder',
    'get_default_cache_path',
    'is_running_in_pytest',
    'remove_cache_folder',
)

_from_json = json.loads if msgspec is None else msgspec.json.decode


# pytest detection

IS_PYTEST: Final[bool] = os.environ.get('PYTEST_VERSION') is not None


def is_running_in_pytest() -> bool:
    return IS_PYTEST


# cache folder path

DEFAULT_CACHE_PATH: Final[Path] = Path('./.valorant_cache')


def get_default_cache_path() -> Path:
    return DEFAULT_CACHE_PATH


def create_cache_folder(cache_path: str | Path) -> Path:
    """
    Create a cache folder with .gitignore to exclude it from version control.

    Parameters
    ----------
    cache_path : str | Path
        Path to the cache folder.

    Returns:
    -------
    Path
        The created cache folder path
    """
    if isinstance(cache_path, str):
        cache_path = Path(cache_path)

    cache_path.mkdir(parents=True, exist_ok=True)

    gitignore_path = cache_path / '.gitignore'
    if not gitignore_path.exists():
        gitignore_content = '# Ignore all files in this cache directory\n*\n'
        gitignore_path.write_text(gitignore_content)

    return cache_path


def remove_cache_folder(cache_path: str | Path) -> None:
    """
    Remove the cache folder and its contents.

    Parameters
    ----------
    cache_path : str | Path
        Path to the cache folder.
    """
    if isinstance(cache_path, str):
        cache_path = Path(cache_path)

    if cache_path.exists() and cache_path.is_dir():
        shutil.rmtree(cache_path)
