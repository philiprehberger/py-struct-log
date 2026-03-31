# philiprehberger-struct-log

[![Tests](https://github.com/philiprehberger/py-struct-log/actions/workflows/publish.yml/badge.svg)](https://github.com/philiprehberger/py-struct-log/actions/workflows/publish.yml)
[![PyPI version](https://img.shields.io/pypi/v/philiprehberger-struct-log.svg)](https://pypi.org/project/philiprehberger-struct-log/)
[![Last updated](https://img.shields.io/github/last-commit/philiprehberger/py-struct-log)](https://github.com/philiprehberger/py-struct-log/commits/main)

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

### Scoped context

Use `log_context` as a context manager for nested scoped context. On exit, the previous context is automatically restored.

```python
from philiprehberger_struct_log import get_logger, log_context

logger = get_logger("myapp")

with log_context(request_id="abc"):
    logger.info("handling")  # includes request_id
    with log_context(user_id="123"):
        logger.info("auth")  # includes request_id AND user_id
    logger.info("done")  # only request_id
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
| `log_context(**kwargs)` | Context manager that merges kwargs into context on enter and restores previous context on exit. Supports nesting. |
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

## Support

If you find this project useful:

⭐ [Star the repo](https://github.com/philiprehberger/py-struct-log)

🐛 [Report issues](https://github.com/philiprehberger/py-struct-log/issues?q=is%3Aissue+is%3Aopen+label%3Abug)

💡 [Suggest features](https://github.com/philiprehberger/py-struct-log/issues?q=is%3Aissue+is%3Aopen+label%3Aenhancement)

❤️ [Sponsor development](https://github.com/sponsors/philiprehberger)

🌐 [All Open Source Projects](https://philiprehberger.com/open-source-packages)

💻 [GitHub Profile](https://github.com/philiprehberger)

🔗 [LinkedIn Profile](https://www.linkedin.com/in/philiprehberger)

## License

[MIT](LICENSE)
