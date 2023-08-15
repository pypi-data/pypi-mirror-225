import warnings as w

w.filterwarnings('ignore', module='pydantic')  # Warning of lxml.etree.E.default() as default in model

from typing import Dict, Union, List

from lxml.builder import E
from lxml.etree import _Element
from pydantic import ConfigDict, BaseModel, Field


class BaseActionOutputModel(BaseModel):
    url: str = Field(
        "",
        description="URL",
    )
    status_code: int = Field(
        -1,
        description="status code",
    )


class BaseHttpActionOutputModel(BaseActionOutputModel):
    headers: Dict = Field(
        {},
        description="headers",
    )


class JsonHttpActionOutputModel(BaseHttpActionOutputModel):
    body: Union[List,Dict] = Field(
        {},
        description="body",
    )


class XmlHttpActionOutputModel(BaseHttpActionOutputModel):
    # FIXME
    model_config = ConfigDict(arbitrary_types_allowed=True)

    body: _Element = Field(
        E.default(),
        description="body",
        # FIXME
        exclude=True,
    )


class JsonRpcWebSocketActionOutputModel(BaseActionOutputModel):
    pass


w.filterwarnings('default')  # Reset
