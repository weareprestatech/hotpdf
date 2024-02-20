import re
from typing import Optional

from ..exceptions.custom_exceptions import DecoderNotInitalised
from .types import EncodingTypes


class Decoder:
    """If there are no embedded fonts, pdfminer.six has issues with
    mapping cid values to their specific unicode characters.
    In that case, we manually override the (cid:int) values
    """

    __cid_mapping: dict[int, str] = {}
    initialised: bool = False

    def __init__(self, charset: Optional[EncodingTypes] = None) -> None:
        if not charset:
            return
        if charset.value in EncodingTypes._value2member_map_:
            self.initialised = True
        if charset == EncodingTypes.LATIN:
            from .mappings.latin import CID_TO_STR

            self.__cid_mapping = CID_TO_STR
        if not self.initialised:
            raise DecoderNotInitalised("Decoder not initialised")

    def cid_str_to_str(self, cid_str: str) -> str:
        """Converts a (cid:int) notation to it's corresponding charset unicode
        In case there's no mapping, return a blank string
        """
        cid_digit = re.search(r"\d+", cid_str)
        if not cid_digit:
            return cid_str
        return self.__cid_mapping.get(int(cid_digit.group()), "")
