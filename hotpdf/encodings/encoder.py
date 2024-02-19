import re
from enum import Enum
from typing import Optional


class EncodingType(Enum):
    LATIN = "latin"


class Encoder:
    """If there are no embedded fonts, pdfminer.six has issues with
    mapping cid values to their specific unicode characters.
    In that case, we manually override the (cid:int) values
    """

    __cid_mapping: dict[int, str] = {}
    initialised: bool = False

    def __init__(self, charset: Optional[EncodingType] = None) -> None:
        if not charset:
            return
        if charset.value in EncodingType._value2member_map_:
            self.initialised = True
        if charset == EncodingType.LATIN:
            from .mappings.latin import CID_TO_STR

            self.__cid_mapping = CID_TO_STR

    def cid_str_to_str(self, cid_str: str) -> str:
        """Converts a (cid:int) notation to it's corresponding charset unicode"""
        cid_digit = re.search(r"\d+", cid_str)
        if not cid_digit:
            return cid_str
        unicode_repr = self.__cid_mapping.get(int(cid_digit.group()))
        return unicode_repr if unicode_repr else cid_str
