import logging
from pathlib import Path

class NoStackTraceFilter(logging.Filter):
    """
    Filter that allows only log records without exception information.
    Used to keep application logs clean from stack traces.
    """
    def filter(self, record: logging.LogRecord) -> bool:
        return record.exc_info is None


class StackTraceOnlyFilter(logging.Filter):
    """
    Filter that allows only log records containing exception information.
    Used to isolate stack traces into a dedicated error log.
    """
    def filter(self, record: logging.LogRecord) -> bool:
        return record.exc_info is not None

# Directory for log files (created once at startup)
LOG_DIR = Path.cwd() / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Standardized log message format across all handlers
formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

# Configure root logger as a single source of truth
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)

# Prevent duplicate handler registration on repeated imports
if not root_logger.handlers:

    # Application log without stack traces
    app_handler = logging.FileHandler(LOG_DIR / "app.log", encoding="utf-8")
    app_handler.setLevel(logging.INFO)
    app_handler.setFormatter(formatter)
    app_handler.addFilter(NoStackTraceFilter())

    # Error log containing only stack traces
    error_handler = logging.FileHandler(LOG_DIR / "error.log", encoding="utf-8")
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    error_handler.addFilter(StackTraceOnlyFilter())

    # Console output for developer feedback
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Attach handlers to root logger
    root_logger.addHandler(app_handler)
    root_logger.addHandler(error_handler)
    root_logger.addHandler(console_handler)
