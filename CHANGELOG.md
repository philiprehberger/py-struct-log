# Changelog

## 0.2.1 (2026-03-31)

- Standardize README to 3-badge format with emoji Support section
- Update CI checkout action to v5 for Node.js 24 compatibility

## 0.2.0 (2026-03-27)

- Add `log_context()` context manager for nested scoped context
- Context manager saves/restores previous context on enter/exit
- Supports arbitrary nesting with proper context isolation
- Add `log_context` to `__all__`
- Add `.github/` issue templates, PR template, and Dependabot config
- Update README with full badge set and Support section

## 0.1.0 (2026-03-21)

- Initial release
- `get_logger()` for creating loggers with structured JSON output
- `bind_context()` / `clear_context()` / `get_context()` for thread-local context propagation
- `StructHandler` logging handler with JSON line output
- Extra record attributes merged into JSON output
