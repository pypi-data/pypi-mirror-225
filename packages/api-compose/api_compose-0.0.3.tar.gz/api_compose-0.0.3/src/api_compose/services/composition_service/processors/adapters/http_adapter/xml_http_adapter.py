## TODO: Update XML HTTP Adapter


__all__ = ["XmlHttpAdapter"]

from lxml import etree
from lxml.etree import Element

from api_compose.core.logging import get_logger
from api_compose.services.common.registry.processor_registry import ProcessorRegistry, ProcessorType, \
    PrceossorCategory
from api_compose.services.common.templated_field.templated_field import BaseTemplatedTextField
from api_compose.services.composition_service.models.actions.inputs import XmlHttpActionInputModel
from api_compose.services.composition_service.models.actions.outputs import XmlHttpActionOutputModel
from api_compose.services.composition_service.models.calculated_field.calculated_field import \
    BuiltinCalculatedFieldNameEnum
from api_compose.services.composition_service.processors.adapters.http_adapter.base_http_adapter import BaseHttpAdapter
from api_compose.services.composition_service.registry.calculated_field_registry import CalculatedFieldRegistry

logger = get_logger(name=__name__)


@ProcessorRegistry.set(
    processor_type=ProcessorType.Builtin,
    processor_category=PrceossorCategory.Adapter,
    models=[]
)
class XmlHttpAdapter(BaseHttpAdapter):
    """
    XML Communication over HTTP
    """

    ## FIXME
    DEBUG_OUTPUT_BODY: Element = etree.Element(BaseHttpAdapter.OUTPUT_BODY_KEY)
    ERROR_OUTPUT_BODY: Element = etree.Element(BaseHttpAdapter.OUTPUT_BODY_KEY)

    @CalculatedFieldRegistry.set(name=BuiltinCalculatedFieldNameEnum.HTTP_XML_BODY.value)
    def calculate_body(self, **ctx) -> Element:
        return self.body.render(jinja_engine=self.jinja_engine, jinja_context=self.jinja_context).load().loaded

    def __init__(
            self,
            body: BaseTemplatedTextField,
            *args,
            **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.body = body
        self.required_templated_fields[BuiltinCalculatedFieldNameEnum.HTTP_XML_BODY.value] = self.body

        # values to be set
        self.input: XmlHttpActionInputModel = XmlHttpActionInputModel()
        self.output: XmlHttpActionOutputModel = XmlHttpActionOutputModel()

    def _set_input(self):
        self.input = XmlHttpActionInputModel(
            url=self.calculated_field_registry.get_value_by_name(BuiltinCalculatedFieldNameEnum.URL.value),
            method=self.calculated_field_registry.get_value_by_name(BuiltinCalculatedFieldNameEnum.HTTP_METHOD.value),
            headers=self.calculated_field_registry.get_value_by_name(BuiltinCalculatedFieldNameEnum.HTTP_HEADERS.value),
            params=self.calculated_field_registry.get_value_by_name(BuiltinCalculatedFieldNameEnum.HTTP_PARAMS.value),
            body=self.calculated_field_registry.get_value_by_name(BuiltinCalculatedFieldNameEnum.HTTP_XML_BODY.value),
        )

    def _set_output(self):
        self.output = XmlHttpActionOutputModel(
            url=self.response.url,
            status_code=self.response.status_code,
            headers=self.response.headers,
            body=self.response.text,
        )
