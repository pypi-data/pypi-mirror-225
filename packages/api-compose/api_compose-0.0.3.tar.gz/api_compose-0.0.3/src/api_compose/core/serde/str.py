import json
from typing import Union, Dict, List

from api_compose.core.serde.base import BaseSerde


class StringSerde(BaseSerde):


    @classmethod
    def deserialise(cls, text: str) -> str:
        return str(text)

    @classmethod
    def serialise(cls, obj: str) -> str:
        return str(obj)
