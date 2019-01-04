from __future__ import annotations

import io
import json
import logging

from philiprehberger_struct_log import (
    StructHandler,
    bind_context,
    clear_context,
    get_context,
    get_logger,
)


def _make_logger(name: str) -> tuple[logging.Logger, io.StringIO]:
    """Create a logger that writes to a StringIO buffer and return both."""
    buf = io.StringIO()
    logger = logging.getLogger(name)
    logger.handlers.clear()
    logger.setLevel(logging.DEBUG)
    handler = StructHandler(stream=buf)
    logger.addHandler(handler)
    return logger, buf


def _parse(buf: io.StringIO) -> dict:
    """Parse the first JSON line from the buffer."""
    buf.seek(0)
    return json.loads(buf.readline())


def test_get_logger_returns_logger() -> None:
    logger = get_logger("test.returns")
    assert isinstance(logger, logging.Logger)
    assert logger.name == "test.returns"
    assert logger.level == logging.DEBUG
    assert any(isinstance(h, StructHandler) for h in logger.handlers)
    logger.handlers.clear()


def test_get_logger_does_not_duplicate_handler() -> None:
    logger = get_logger("test.nodup")
    handler_count = sum(1 for h in logger.handlers if isinstance(h, StructHandler))
    get_logger("test.nodup")
    assert sum(1 for h in logger.handlers if isinstance(h, StructHandler)) == handler_count
    logger.handlers.clear()


def test_bind_context_and_get_context() -> None:
    clear_context()
    bind_context(request_id="abc-123", user="alice")
    ctx = get_context()
    assert ctx == {"request_id": "abc-123", "user": "alice"}
    clear_context()


def test_clear_context() -> None:
    bind_context(key="value")
    clear_context()
    assert get_context() == {}


def test_get_context_returns_copy() -> None:
    clear_context()
    bind_context(x=1)
    ctx = get_context()
    ctx["x"] = 999
    assert get_context()["x"] == 1
    clear_context()


def test_struct_handler_outputs_json() -> None:
    logger, buf = _make_logger("test.json_output")
    logger.info("hello structured")
    entry = _parse(buf)
    assert isinstance(entry, dict)
    assert entry["message"] == "hello structured"
    assert entry["level"] == "INFO"
    assert entry["logger"] == "test.json_output"
    assert "timestamp" in entry
    logger.handlers.clear()


def test_context_appears_in_log_output() -> None:
    clear_context()
    bind_context(request_id="req-42", service="api")
    logger, buf = _make_logger("test.context_in_log")
    logger.info("with context")
    entry = _parse(buf)
    assert entry["request_id"] == "req-42"
    assert entry["service"] == "api"
    logger.handlers.clear()
    clear_context()


def test_extra_record_attributes_in_output() -> None:
    logger, buf = _make_logger("test.extra_attrs")
    logger.info("with extra", extra={"trace_id": "tr-999"})
    entry = _parse(buf)
    assert entry["trace_id"] == "tr-999"
    logger.handlers.clear()


def test_timestamp_is_iso_format() -> None:
    logger, buf = _make_logger("test.timestamp")
    logger.info("check ts")
    entry = _parse(buf)
    assert "T" in entry["timestamp"]
    assert entry["timestamp"].endswith("+00:00")
    logger.handlers.clear()
