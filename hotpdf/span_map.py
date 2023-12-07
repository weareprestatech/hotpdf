from .data.classes import HotCharacter
from collections import defaultdict


class SpanMap:
    """
    Hashmap to store spans and their child words for fast referencing
    and character grouping.
    """

    def __init__(self):
        self.map = defaultdict(list)

    def insert(self, span_id: str, hot_character: HotCharacter):
        if span_id:
            self.map[span_id].append(hot_character)

    def get_span(self, span_id: str) -> list[HotCharacter]:
        return self.map.get(span_id)
