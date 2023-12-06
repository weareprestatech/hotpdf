from .data.classes import HotCharacter
from collections import defaultdict


class SpanMap:
    def __init__(self):
        self.map = defaultdict(list)

    def insert(self, span_id: str, hot_character: HotCharacter):
        self.map[span_id].append(hot_character)

    def get_span(self, span_id: str) -> list[HotCharacter]:
        return self.map.get(span_id)
