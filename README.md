# philiprehberger-struct-log

[![Tests](https://github.com/philiprehberger/py-struct-log/actions/workflows/publish.yml/badge.svg)](https://github.com/philiprehberger/py-struct-log/actions/workflows/publish.yml)
[![PyPI version](https://img.shields.io/pypi/v/philiprehberger-struct-log.svg)](https://pypi.org/project/philiprehberger-struct-log/)
[![License](https://img.shields.io/github/license/philiprehberger/py-struct-log)](LICENSE)
[![Sponsor](https://img.shields.io/badge/sponsor-GitHub%20Sponsors-ec6cb9)](https://github.com/sponsors/philiprehberger)

Structured JSON logging with automatic context propagation.

## Installation

```bash
pip install philiprehberger-struct-log
```

## Usage

### Basic logging

```python
from philiprehberger_struct_log import get_logger

logger = get_logger("myapp")
logger.info("Server started", extra={"port": 8080})
# {"timestamp": "2026-03-21T12:00:00+00:00", "level": "INFO", "message": "Server started", "logger": "myapp", "port": 8080}
```

### Context propagation

```python
from philiprehberger_struct_log import get_logger, bind_context, clear_context

logger = get_logger("myapp")

bind_context(request_id="abc-123", user="alice")
logger.info("Processing request")
# {"timestamp": "...", "level": "INFO", "message": "Processing request", "logger": "myapp", "request_id": "abc-123", "user": "alice"}

clear_context()
```

### Inspecting context

```python
from philiprehberger_struct_log import bind_context, get_context

bind_context(service="api", env="production")
ctx = get_context()
# {"service": "api", "env": "production"}
```

## API

| Name | Description |
|---|---|
| `get_logger(name)` | Get or create a logger with a `StructHandler` attached. Level is set to `DEBUG`. |
| `bind_context(**kwargs)` | Store key-value pairs in thread-local context. Included in every log entry on the current thread. |
| `clear_context()` | Clear all bound context for the current thread. |
| `get_context()` | Return a copy of the current thread-local context as a dict. |
| `StructHandler(stream=None)` | Logging handler that formats records as JSON lines. Defaults to stderr. |

### JSON output fields

| Field | Description |
|---|---|
| `timestamp` | ISO 8601 UTC timestamp |
| `level` | Log level name (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`) |
| `message` | Formatted log message |
| `logger` | Logger name |

Bound context fields and any `extra={}` kwargs passed to the log call are merged into the top-level JSON object.

## Development

```bash
pip install -e .
python -m pytest tests/ -v
```

## License

MIT
