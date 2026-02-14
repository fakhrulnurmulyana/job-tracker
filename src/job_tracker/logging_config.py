import logging
from pathlib import Path

class NoStackTraceFilter(logging.Filter):
    """
    Logging filter that allows only records without exception information.

    This filter is typically applied to application logs to keep
    normal log messages clean from stack traces.
    """
    def filter(self, record: logging.LogRecord) -> bool:
        """
        Determine if a log record should be processed.

        Args:
            record (logging.LogRecord): The log record to evaluate.

        Returns:
            bool: True if the record has no exception info, False otherwise.
        """
        return record.exc_info is None


class StackTraceOnlyFilter(logging.Filter):
    """
    Logging filter that allows only records containing exception information.

    This filter is used to isolate stack traces into a dedicated error log.
    """
    def filter(self, record: logging.LogRecord) -> bool:
        """
        Determine if a log record should be processed.

        Args:
            record (logging.LogRecord): The log record to evaluate.

        Returns:
            bool: True if the record contains exception info, False otherwise.
        """
        return record.exc_info is not None
    

class DebugOnlyFilter(logging.Filter):
    """
    Logging filter that allows only DEBUG-level log records.

    Useful for separating verbose debug logs from info or error logs.
    """
    def filter(self, record: logging.LogRecord) -> bool:
        """
        Determine if a log record should be processed.

        Args:
            record (logging.LogRecord): The log record to evaluate.

        Returns:
            bool: True if the record level is DEBUG, False otherwise.
        """
        return record.levelno == logging.DEBUG
    


# Directory for log files (created once at startup)
LOG_DIR = Path.cwd() / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Standardized log message format across all handlers
formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

# Configure root logger as a single source of truth
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)

# Prevent duplicate handler registration on repeated imports
if not root_logger.handlers:

    # Application log without stack traces
    app_handler = logging.FileHandler(
        LOG_DIR / "app.log", 
        encoding="utf-8",
    )
    app_handler.setLevel(logging.INFO)
    app_handler.setFormatter(formatter)
    app_handler.addFilter(NoStackTraceFilter())

    # Error log containing only stack traces
    error_handler = logging.FileHandler(
        LOG_DIR / "error.log", 
        encoding="utf-8",
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    error_handler.addFilter(StackTraceOnlyFilter())

    debug_handler = logging.FileHandler(
        LOG_DIR / "debug.log",
        encoding="utf-8"
    )
    debug_handler.setLevel(logging.DEBUG)
    debug_handler.setFormatter(formatter)
    debug_handler.addFilter(DebugOnlyFilter())

    # Attach handlers to root logger
    root_logger.addHandler(app_handler)
    root_logger.addHandler(error_handler)
    root_logger.addHandler(debug_handler)
