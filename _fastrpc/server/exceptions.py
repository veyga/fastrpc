from dataclasses import dataclass


@dataclass
class FastRPCException(Exception):
    message: str


__all__ = [
    "FastRPCException",
]
