from dataclasses import dataclass
from typing import Optional, List


@dataclass
class Second:
    value: int


@dataclass
class Firster:
    value: int
    second: Second
    opt: Optional[Second]
    xs: Optional[List[Second]] = None
