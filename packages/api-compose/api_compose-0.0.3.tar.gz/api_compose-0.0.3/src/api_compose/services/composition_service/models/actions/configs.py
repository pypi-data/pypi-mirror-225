from __future__ import annotations

from pydantic import BaseModel as _BaseModel, Field

from api_compose.services.common.templated_field.templated_field import BaseTemplatedTextField, TextFieldFormat, \
    StringTemplatedTextField, JsonLikeTemplatedTextField, JsonTemplatedTextField


class BaseActionConfigModel(_BaseModel, extra='allow'):
    adapter_class_name: str = Field(
        'BaseAdapter',
        description='Adapter Controller Name',
    )

    url: StringTemplatedTextField = Field(
        StringTemplatedTextField(template=''),
        description='Templateable URL',
    )


class JsonHttpActionConfigModel(BaseActionConfigModel):
    adapter_class_name: str = Field(
        'JsonHttpAdapter',
        description=BaseActionConfigModel.model_fields['adapter_class_name'].description,
    )
    method: StringTemplatedTextField = Field(
        StringTemplatedTextField(template='GET'),
        description='Templateable HTTP Method',
    )
    headers: JsonLikeTemplatedTextField = Field(
        JsonTemplatedTextField(template="{}"),
        description='Templateable HTTP Headers',
    )
    params: JsonLikeTemplatedTextField = Field(
        JsonTemplatedTextField(template="{}"),
        description='Templateable HTTP Params',
    )
    body: JsonLikeTemplatedTextField = Field(
        JsonTemplatedTextField(template="{}"),
        description='Templateable HTTP body',
    )


class JsonRpcWebSocketActionConfigModel(BaseActionConfigModel):
    pass
