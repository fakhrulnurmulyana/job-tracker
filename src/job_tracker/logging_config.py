import logging
from pathlib import Path

class NoStackTraceFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return record.exc_info is None


class StackTraceOnlyFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return record.exc_info is not None

LOG_DIR = Path.cwd() / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)

if not root_logger.handlers:

    app_handler = logging.FileHandler(LOG_DIR / "app.log", encoding="utf-8")
    app_handler.setLevel(logging.INFO)
    app_handler.setFormatter(formatter)
    app_handler.addFilter(NoStackTraceFilter())

    error_handler = logging.FileHandler(LOG_DIR / "error.log", encoding="utf-8")
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    error_handler.addFilter(StackTraceOnlyFilter())

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    root_logger.addHandler(app_handler)
    root_logger.addHandler(error_handler)
    root_logger.addHandler(console_handler)
