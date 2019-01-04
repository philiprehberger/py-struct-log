"""Structured JSON logging with automatic context propagation."""

from __future__ import annotations

import json
import logging
import sys
import threading
from datetime import datetime, timezone
from typing import Any

__all__ = ["get_logger", "bind_context", "clear_context", "get_context", "StructHandler"]

_context = threading.local()

_BUILTIN_ATTRS = frozenset(logging.LogRecord("", 0, "", 0, None, None, None).__dict__)


def bind_context(**kwargs: Any) -> None:
    """Store key-value pairs in thread-local context.

    These fields are automatically included in every log entry
    emitted by a ``StructHandler`` on the current thread.
    """
    if not hasattr(_context, "data"):
        _context.data = {}
    _context.data.update(kwargs)


def clear_context() -> None:
    """Clear all bound context for the current thread."""
    _context.data = {}


def get_context() -> dict[str, Any]:
    """Return a copy of the current thread-local context."""
    if not hasattr(_context, "data"):
        return {}
    return dict(_context.data)


class StructHandler(logging.Handler):
    """Logging handler that formats records as JSON lines.

    Each log entry includes a timestamp, level, message, logger name,
    any bound thread-local context, and any extra fields from the record.
    """

    def __init__(self, stream: Any | None = None) -> None:
        super().__init__()
        self.stream = stream or sys.stderr

    def emit(self, record: logging.LogRecord) -> None:
        try:
            entry: dict[str, Any] = {
                "timestamp": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
                "level": record.levelname,
                "message": record.getMessage(),
                "logger": record.name,
            }

            # Merge bound context
            ctx = get_context()
            if ctx:
                entry.update(ctx)

            # Merge extra fields from the record
            for key, value in record.__dict__.items():
                if key not in _BUILTIN_ATTRS and key not in entry:
                    entry[key] = value

            line = json.dumps(entry, default=str)
            self.stream.write(line + "\n")
            self.stream.flush()
        except Exception:
            self.handleError(record)


def get_logger(name: str) -> logging.Logger:
    """Get or create a logger with a ``StructHandler`` attached.

    If the logger already has a ``StructHandler``, no additional handler
    is added.  The logger level is set to ``DEBUG``.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not any(isinstance(h, StructHandler) for h in logger.handlers):
        logger.addHandler(StructHandler())

    return logger
