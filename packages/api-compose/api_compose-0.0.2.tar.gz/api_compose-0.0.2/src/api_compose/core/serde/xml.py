import traceback

from lxml import etree
from lxml.builder import E
from lxml.etree import XMLSyntaxError, _Element

from api_compose.core.logging import get_logger
from api_compose.core.serde.base import BaseSerde

logger = get_logger(__name__)


class XmlSerde(BaseSerde):
    @classmethod
    def deserialise(cls, text: str) -> _Element:
        try:
            return etree.fromstring(text)
        except XMLSyntaxError as e:
            logger.error(traceback.format_exc())
            return E.default()

    @classmethod
    def serialise(cls, obj: _Element) -> str:
        return etree.tostring(obj)
