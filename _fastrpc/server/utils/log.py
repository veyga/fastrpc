import coloredlogs, logging

logger = logging.getLogger("fastrpc")
coloredlogs.install(level="DEBUG")

__all__ = [
    "logger",
]
