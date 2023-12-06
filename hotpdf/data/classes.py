from dataclasses import dataclass
from typing import Optional


@dataclass
class HotCharacter:
    value: str
    x: int
    y: int
    x_end: float
    span_id: Optional[str]
