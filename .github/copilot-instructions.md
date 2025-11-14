# Valorant.py AI Coding Instructions

## Project Overview
An async Python wrapper for the [Valorant API](https://valorant-api.com) using Pydantic V2 models and aiohttp. Features SQLite-based HTTP caching (enabled by default) via `aiohttp-client-cache`.

## Architecture

### Core Components
- **`valorant/client.py`**: Main `Client` class providing async context manager for API access. Methods follow pattern `fetch_<resource>()` (single) and `fetch_<resources>()` (list).
- **`valorant/http.py`**: `HTTPClient` handles all HTTP requests via `Route` class. Manages caching through `CachedSession` or plain `ClientSession`.
- **`valorant/models/`**: Pydantic V2 models for API responses. All inherit from `BaseModel` or `BaseUUIDModel` (in `base.py`).
- **`valorant/utils.py`**: Cache management utilities (`create_cache_folder`, `remove_cache_folder`) and JSON parsing (msgspec when available, fallback to stdlib).

### Data Flow
1. Client method → HTTPClient.request() → Route.url
2. Response → Pydantic `Response[T]` wrapper → `.data` extraction
3. Cache stored in `./.valorant_cache/aiohttp-cache.db` (SQLite) with 24hr TTL default

## Development Workflow

### Setup & Dependencies
```bash
make sync              # Install all dependencies with uv
```

## Style notes
- Write comments as full sentences and end them with a period.

### Testing
```bash
make tests             # Run pytest with coverage (-n auto for parallel)
make report            # View coverage report after tests
```
- Use `pytest` style tests, not `unittest` style
- Prefer function-based tests over class-based tests unless you need to share setup/teardown code.
- Add focused unit tests for new behavior and edge cases; keep tests deterministic.
- Test files should follow the naming convention `test_*.py`
- All functions and methods must have type annotations.
- If you import a module only for its types, put the import inside an `if TYPE_CHECKING` block.
- Use `@pytest.mark.anyio` for async tests.
- Use `@pytest.mark.parametrize` for parameterized tests.
- Use `@pytest.fixture` to create reusable test fixtures.
- Use `pytest.raises` to check for exceptions.
- Use `monkeypatch` fixture to modify environment variables or attributes during tests.

## Docstring guidelines
- Use Google style docstrings.
- For examples in docstrings, always use Python code blocks with proper syntax highlighting:
  ```python
  # Good: Use code blocks for examples
  def example_function() -> None:
      """Example function with proper code block.
      
      Example:
          ```python
          result = example_function()
          print(result)
          ```
      """
      pass
  ```
- Avoid doctest format (`>>> `) or plain text examples in docstrings.
- Code examples should be clean, properly indented, and ready to run.

### Code Quality
```bash
make check             # Run format-check, lint, mypy, and tests
make format            # Auto-fix with ruff
make lint              # Check with ruff (no fixes)
make mypy              # Type checking (strict mode)
```

## What reviewers look for

- Tests covering new behaviour.
- Consistent style: code formatted with `uv run ruff format`, imports sorted, and type hints passing `uv run mypy .`.
- Clean history and a helpful PR description.

## Coding Conventions

### Style & Formatting
- **Quotes**: Single quotes for strings (`'text'`, not `"text"`)
- **Line length**: 120 characters (ruff configured)
- **Imports**: Combine with `from __future__ import annotations` at top, use TYPE_CHECKING blocks
- **Type hints**: Mandatory (mypy strict mode). Use `TypeAlias` for complex types.

### Pydantic Models
- **Field aliases**: Use `Field(alias='camelCase')` for API's camelCase → snake_case mapping
  ```python
  display_name: str = Field(alias='displayName')
  fire_rate: float = Field(alias='fireRate')
  ```
- **Base classes**: 
  - `BaseModel` for general models (auto-forbids extra fields in tests via `is_running_in_pytest()`)
  - `BaseUUIDModel` for UUID-keyed resources (implements `__eq__`, `__hash__`)
- **Localization**: Use `LocalizedField` for multi-language strings (e.g., `display_name: str | LocalizedField`)

### Error Handling
- Custom exceptions in `errors.py`: `ValorantError`, `HTTPException`, `NotFound`
- Raise `NotFound` for 404 responses (see `http.py` line 149)

### Cache Implementation
- Check if `enable_cache=True` in Client/HTTPClient init
- Use `utils.create_cache_folder()` to create cache dir with `.gitignore`
- Cache path defaults to `./.valorant_cache`, customizable via `cache_path` param
- Tests verify `CachedSession` vs `ClientSession` based on `enable_cache` flag

### Enums
- Custom `StrEnum` for Python 3.10 compatibility (stdlib `StrEnum` available 3.11+)
- Values often match Valorant's internal enum format: `'ECompetitiveDivision::GOLD'`

## Common Pitfalls
- **Don't** create separate `close()` calls for models - only Client manages session lifecycle
- **Don't** use `json.dumps()` directly - use `utils._from_json()` which prefers msgspec for speed
- **Remember** `Client.clear()` resets closed state but doesn't create new session (requires `start()`)
- **Models in tests**: Extra fields are forbidden (`extra='forbid'`) to catch API changes

## Key Files
- `valorant/models/base.py` - Base model classes and `Response[T]` generic
- `valorant/enums.py` - All enum types (Language, WeaponCategory, etc.)
- `tests/conftest.py` - Shared pytest fixtures (client, cache_path)
- `pyproject.toml` - Ruff rules, mypy config, pytest options

## Optional Features
- **Speed**: Install with `[speed]` extra for msgspec JSON parsing (not supported on Python 3.14/3.14t)
