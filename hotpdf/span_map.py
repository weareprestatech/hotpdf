from .data.classes import HotCharacter
from collections import defaultdict
from typing import Union


class SpanMap:
    """
    Hashmap to store spans and their child words for fast referencing
    and character grouping.
    """

    def __init__(self):
        self.map = defaultdict(list)

    def __getitem__(self, span_id: str) -> Union[list[HotCharacter], None]:
        return self.get_span(span_id)

    def __setitem__(self, span_id: Union[str, None], hot_character: HotCharacter):
        if not span_id:
            raise KeyError("Cannot set key as None")
        self.insert(span_id, hot_character)

    def insert(self, span_id: str, hot_character: HotCharacter):
        if span_id:
            self.map[span_id].append(hot_character)

    def get_span(self, span_id: Union[str, None]) -> Union[list[HotCharacter], None]:
        if span_id:
            return self.map.get(span_id)
        return None
