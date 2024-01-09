from .data.classes import HotCharacter, Span
from typing import Union, Iterable


class SpanMap:
    """
    Hashmap to store spans and their child words for fast referencing
    and character grouping.
    Keys are span_ids and values are Span objects.
    """

    def __init__(self) -> None:
        self.map: dict[str, Span] = dict()

    def __len__(self) -> int:
        return len(self.map)

    def __getitem__(self, span_id: str) -> Union[Span, None]:
        return self.get_span(span_id)

    def __setitem__(
        self, span_id: Union[str, None], hot_character: HotCharacter
    ) -> None:
        self.insert(span_id, hot_character)

    def items(self) -> Iterable[tuple[str, Span]]:
        return self.map.items()

    def insert(self, span_id: Union[str, None], hot_character: HotCharacter) -> None:
        if not span_id:
            raise KeyError("Cannot set key as None")
        if span_id in self.map:
            span = self.map[span_id]
            assert span.x0 <= hot_character.x
            assert span.y0 == hot_character.y
            span.characters.append(hot_character)
            if hot_character.x_end > span.x_end:
                span.x_end = hot_character.x_end
        else:
            span = Span(
                characters=[hot_character],
                x0=hot_character.x,
                y0=hot_character.y,
                x_end=hot_character.x_end,
                span_id=span_id,
            )

        self.map[span_id] = span

    def get_span(self, span_id: Union[str, None]) -> Union[Span, None]:
        if span_id:
            return self.map.get(span_id)
        return None
