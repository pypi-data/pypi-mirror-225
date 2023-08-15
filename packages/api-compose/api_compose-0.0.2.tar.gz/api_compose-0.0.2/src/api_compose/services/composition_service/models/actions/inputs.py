import warnings as w

w.filterwarnings('ignore', module='pydantic')  # Warning of lxml.etree.E.default() as default in model

from typing import Dict

from lxml.builder import E
from lxml.etree import _Element
from pydantic import BaseModel as _BaseModel, Field, ConfigDict, field_validator


class BaseActionInputModel(_BaseModel):
    url: str = Field(
        "",
        description='URL',
    )

class BaseHttpActionInputModel(BaseActionInputModel):
    method: str = Field(
        '',
        description="HTTP Method",
    )
    headers: Dict = Field(
        {},
        description='HTTP Header',
    )
    params: Dict = Field(
        {},
        description='HTTP URL params',
    )


class JsonHttpActionInputModel(BaseHttpActionInputModel):
    body: Dict = Field(
        {},
        description='HTTP body',
    )


class XmlHttpActionInputModel(BaseHttpActionInputModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    body: _Element = Field(
        E.default(),
        description='HTTP body',
    )


class JsonRpcWebSocketActionInputModel(BaseActionInputModel):
    pass


w.filterwarnings('default')  # Reset
