__all__ = ["JsonHttpAdapter"]

import json

from api_compose.core.logging import get_logger
from api_compose.services.common.registry.processor_registry import ProcessorRegistry, ProcessorType, \
    PrceossorCategory
from api_compose.services.common.templated_field.templated_field import BaseTemplatedTextField, TextFieldFormat
from api_compose.services.composition_service.models.actions.actions import JsonHttpActionInputModel, \
    JsonHttpActionOutputModel
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
class JsonHttpAdapter(BaseHttpAdapter):
    """
    JSON Communication over HTTP
    """

    DEBUG_OUTPUT_BODY: str = json.dumps({BaseHttpAdapter.OUTPUT_BODY_KEY: 'This is a debug response'})
    ERROR_OUTPUT_BODY: str = json.dumps({BaseHttpAdapter.OUTPUT_BODY_KEY: "failed to parse output"})

    @CalculatedFieldRegistry.set(name=BuiltinCalculatedFieldNameEnum.HTTP_JSON_BODY.value)
    def calculate_body(self, **ctx) -> BaseTemplatedTextField:
        return self.body.render(jinja_engine=self.jinja_engine, jinja_context=self.jinja_context).load().loaded

    def __init__(
            self,
            body: BaseTemplatedTextField,
            *args,
            **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.body = body
        self.required_templated_fields[BuiltinCalculatedFieldNameEnum.HTTP_JSON_BODY.value] = self.body

        # values to be set
        self.input: JsonHttpActionInputModel = JsonHttpActionInputModel()
        self.output: JsonHttpActionOutputModel = JsonHttpActionOutputModel()

    def _set_input(self):
        self.input = JsonHttpActionInputModel(
            url=self.calculated_field_registry.get_value_by_name(BuiltinCalculatedFieldNameEnum.URL.value),
            method=self.calculated_field_registry.get_value_by_name(BuiltinCalculatedFieldNameEnum.HTTP_METHOD.value),
            headers=self.calculated_field_registry.get_value_by_name(BuiltinCalculatedFieldNameEnum.HTTP_HEADERS.value),
            params=self.calculated_field_registry.get_value_by_name(BuiltinCalculatedFieldNameEnum.HTTP_PARAMS.value),
            body=self.calculated_field_registry.get_value_by_name(BuiltinCalculatedFieldNameEnum.HTTP_JSON_BODY.value),
        )

    def _set_output(self):
        try:
            body = json.loads(self.response.text)
        except Exception as e:
            logger.error("Cannot deserialise output body to Dict \n"
                         f"{self.response.text}")
            body = {'message': self.response.text}

        self.output = JsonHttpActionOutputModel(
            url=self.response.url,
            status_code=self.response.status_code,
            headers=dict(self.response.headers),
            body=body,
        )
