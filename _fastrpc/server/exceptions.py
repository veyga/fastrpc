from dataclasses import dataclass


@dataclass
class FastRPCException(Exception):
    message: str

    def __post_init__(self):
        super().__init__(self.message)


__all__ = [
    "FastRPCException",
]
