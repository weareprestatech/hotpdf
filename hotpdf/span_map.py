from typing import Iterable, Union

from .data.classes import HotCharacter, Span


class SpanMap:
    """
    Hashmap to store spans and their child words for fast referencing
    and character grouping.
    Keys are span_ids and values are Span objects.
    """

    def __init__(self) -> None:
        self.span_map: dict[str, Span] = dict()

    def __len__(self) -> int:
        return len(self.span_map)

    def __getitem__(self, span_id: str) -> Union[Span, None]:
        return self.get_span(span_id)

    def __setitem__(self, span_id: Union[str, None], hot_character: HotCharacter) -> None:
        self.insert(span_id, hot_character)

    def items(self) -> Iterable[tuple[str, Span]]:
        return self.span_map.items()

    def insert(self, span_id: Union[str, None], hot_character: HotCharacter) -> None:
        if not span_id:
            raise KeyError("Cannot set key as None")
        if span_id in self.span_map:
            span = self.span_map[span_id]
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

        self.span_map[span_id] = span

    def get_span(self, span_id: Union[str, None]) -> Union[Span, None]:
        if span_id:
            return self.span_map.get(span_id)
        return None
