from dataclasses import dataclass
from typing import Optional


@dataclass
class HotCharacter:
    value: str
    x: int
    y: int
    x_end: float
    span_id: Optional[str] = None


@dataclass
class ElementDimension:
    x0: int
    y0: int
    x1: int
    y1: int
    span_id: Optional[str] = None
