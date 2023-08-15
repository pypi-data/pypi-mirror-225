from enum import Enum
from typing import Any, Union, Optional, Literal

from pydantic import BaseModel as _BaseModel, Field
from pydantic import field_serializer

from api_compose.core.jinja.core.context import BaseJinjaContext
from api_compose.core.jinja.core.engine import JinjaEngine
from api_compose.core.jinja.exceptions import FailedToRenderTemplateException
from api_compose.core.logging import get_logger
from api_compose.core.serde.base import BaseSerde
from api_compose.core.serde.integer import IntegerSerde
from api_compose.core.serde.json import JsonSerde
from api_compose.core.serde.str import StringSerde
from api_compose.core.serde.xml import XmlSerde
from api_compose.core.serde.yaml import YamlSerde
from api_compose.services.common.events.templated_field import TemplatedFieldEvent

logger = get_logger(__name__)


class TextFieldFormat(str, Enum):
    STRING = 'string'
    INTEGER = 'integer'
    YAML = 'yaml'
    JSON = 'json'
    XML = 'xml'


class BaseTemplatedTextField(_BaseModel):
    template: str = ""
    format: TextFieldFormat
    serde: BaseSerde = Field(exclude=True)

    @field_serializer('serde')
    def serialize_serde(self, serde: BaseSerde, _info):
        return serde.__str__()

    # Other properties
    rendered: Optional[str] = Field(None, exclude=True )
    loaded: Optional[Any] = Field(None, exclude=True )

    # Setters
    def render(self, jinja_engine: JinjaEngine, jinja_context: BaseJinjaContext):
        # Step 1: render string

        rendered, is_success, exec = jinja_engine.set_template_by_string(self.template).render_to_str(
            jinja_context)

        if not is_success:
            # raise instead?
            logger.error(f"{self.template=}", TemplatedFieldEvent())
            logger.error(f"{is_success=}", TemplatedFieldEvent())
            logger.error(f"Exception Message={str(exec)}", TemplatedFieldEvent())

            logger.error(f"Available Globals {jinja_engine._custom_global_keys=}", TemplatedFieldEvent())
            raise FailedToRenderTemplateException(
                template=self.template,
                exec=exec,
                custom_global_keys=jinja_engine._custom_global_keys)

        self.rendered = rendered
        return self

    def load(self):
        try:
            self.loaded = self.serde.deserialise(self.rendered)
        except Exception as e:
            logger.error(f"Error loading string as {self.format} \n"
                         f"{self.rendered=}")
            raise
        return self


class StringTemplatedTextField(BaseTemplatedTextField):
    format: Literal[TextFieldFormat.STRING] = TextFieldFormat.STRING

    serde: StringSerde = Field(
        StringSerde(),
        exclude=True
    )


class IntegerTemplatedTextField(BaseTemplatedTextField):
    format: Literal[TextFieldFormat.INTEGER] = TextFieldFormat.INTEGER

    serde: IntegerSerde = Field(
        IntegerSerde(),
        exclude=True
    )


class YamlTemplatedTextField(BaseTemplatedTextField):
    format: Literal[TextFieldFormat.YAML] = TextFieldFormat.YAML

    serde: YamlSerde = Field(
        YamlSerde(),
        exclude=True
    )


class JsonTemplatedTextField(BaseTemplatedTextField):
    format: Literal[TextFieldFormat.JSON] = TextFieldFormat.JSON

    serde: JsonSerde = Field(
        JsonSerde(),
        exclude=True
    )


class XmlTemplatedTextField(BaseTemplatedTextField):
    format: Literal[TextFieldFormat.XML] = TextFieldFormat.XML
    serde: XmlSerde = Field(
        XmlSerde(),
        exclude=True,
    )


JsonLikeTemplatedTextField = Union[JsonTemplatedTextField, YamlTemplatedTextField]
