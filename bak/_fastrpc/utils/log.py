import logging
import logging.config
from contextlib import contextmanager
from enum import StrEnum
from types import SimpleNamespace as ___
from typing import Optional


class LoggerName(StrEnum):
    ROOT = "root"
    SIMPLE = "simple"
    COLORED = "colored"


Logger = ___(
    ROOT=logging.getLogger(LoggerName.ROOT),
    SIMPLE=logging.getLogger(LoggerName.SIMPLE),
    COLORED=logging.getLogger(LoggerName.COLORED),
)


def create_logger(
    name: str = LoggerName.ROOT, propogate: bool = False
) -> logging.Logger:
    """
    Returns a logger with the corresponding 'logconfig' applied
    [best used in scripts]
    """
    logging.config.fileConfig("logconfig")
    logger = logging.getLogger(name)
    logger.propagate = propogate
    return logger


class RootFormatter(logging.Formatter):
    """[%LEVEL%] %MESSAGE%"""

    def format(self, record):
        return f"[{record.levelname}] {record.getMessage()}"


class SimpleFormatter(logging.Formatter):
    """%MESSAGE%"""

    def format(self, record):
        return record.getMessage()


class ColoredFormatter(logging.Formatter):
    """%%MESSAGE% (with colors)"""

    COLOR_CODES = {
        "DEBUG": "\033[1;34m",  # Blue
        "INFO": "\033[1;32m",  # Green
        "WARNING": "\033[1;33m",  # Yellow
        "ERROR": "\033[1;31m",  # Red
        "CRITICAL": "\033[1;41m" + "\033[1;37m",  # White on Red background
    }
    RESET_CODE = "\033[0m"

    def format(self, record):
        log_level = record.levelname
        message = super().format(record)
        return f"{self.COLOR_CODES.get(log_level, '')}{message}{self.RESET_CODE}"


@contextmanager
def tee_logs(
    *output_streams,
    logger: logging.Logger,
    level: int = logging.INFO,
    formatter: Optional[type] = None,
):
    """Tees the output of given logger name to the specified output streams."""
    handlers = [logging.StreamHandler(os) for os in output_streams]
    for handler in handlers:
        handler.setLevel(level)
        if formatter:
            handler.setFormatter(formatter())
        logger.addHandler(handler)
    yield
    for handler in handlers:
        handler.flush()
        logger.removeHandler(handler)
        handler.close()
