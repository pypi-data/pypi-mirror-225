from enum import Enum
from typing import Optional

from pydantic import ConfigDict, Field

from api_compose.services.assertion_service.models.configs import JinjaAssertionConfigModel, \
    PythonAssertionConfigModel, BaseAssertionConfigModel
from api_compose.services.common.models.base import BaseModel


class AssertionState(str, Enum):
    PENDING = 'pending'
    EXECUTED = 'executed'


class BaseAssertionModel(BaseModel):
    id: str = 'BaseAssertionModel'
    class_name: str = 'TestItemController'
    description: str = 'Placeholder for Base Test Item'
    state: AssertionState = Field(AssertionState.PENDING, description='State of the Test Item')
    is_success: bool = Field(False, description='whether the test item is successful')
    exec: Optional[str] = Field(None, description='(If any) Exception raised when test item is executed')

    config: BaseAssertionConfigModel
    model_config = ConfigDict(arbitrary_types_allowed=True)


class JinjaAssertionModel(BaseAssertionModel):
    id: str = 'JinjaAssertionModel'
    class_name: str = "JinjaAssertion"
    description: str = 'Test Item in Jinja'
    config: JinjaAssertionConfigModel


class PythonAssertionModel(BaseAssertionModel):
    id: str = 'PythonAssertionModel'
    class_name: str = "PythonAssertion"
    description: str = 'Test Item in Python'
    config: PythonAssertionConfigModel
