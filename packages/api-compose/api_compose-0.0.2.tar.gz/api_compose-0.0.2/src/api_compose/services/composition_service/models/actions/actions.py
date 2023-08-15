from typing import Union, Optional

from pydantic import Field, model_validator

from api_compose.services.common.models.base import BaseModel
from api_compose.services.composition_service.models.actions.configs import BaseActionConfigModel, \
    JsonHttpActionConfigModel, JsonRpcWebSocketActionConfigModel
from api_compose.services.composition_service.models.actions.inputs import BaseActionInputModel, \
    JsonHttpActionInputModel, \
    JsonRpcWebSocketActionInputModel
from api_compose.services.composition_service.models.actions.outputs import BaseActionOutputModel, \
    JsonHttpActionOutputModel, \
    JsonRpcWebSocketActionOutputModel
from api_compose.services.composition_service.models.actions.states import ActionState
from api_compose.services.composition_service.models.protocols.protocols import ActionAPIProtocol
from api_compose.services.composition_service.models.protocols.status_enums import HttpResponseStatusEnum, \
    WebSocketResponseStatusEnum, \
    OtherResponseStatusEnum


class BaseActionModel(BaseModel):
    """
    Base Action.
    Action should follow the convention

    <MessageFormat><TransportProtocol>Action
    """
    class_name: str = 'Action'
    config: BaseActionConfigModel = Field(
        BaseActionConfigModel(),
        description='Configuration Passed to Adapter to execute the Action',

    )

    # when not set explicitly, same as id. Used to distinguish two or more same actions, but executed in the same test scenario
    execution_id: str = Field(
        None,
        description='Unique Execution Id per scenario',

    )

    @model_validator(mode="before")
    @classmethod
    def check_execution_id(cls, values):
        if not values.get('execution_id'):
            values['execution_id'] = values['id']
        return values

    start_time: float = Field(
        -1,
        description='Start Time, number of seconds passed since epoch',
    )
    end_time: float = Field(
        -1,
        description='End Time, number of seconds passed since epoch',
    )

    @property
    def uid(self):
        """
        Action uses execution_id as unique_id.
        """
        return self.execution_id

    @property
    def elapsed_time(self) -> float:
        """
        Elapsed Seconds
        Returns
        -------

        """
        if self.start_time > 0 and self.end_time > 0:
            return self.end_time - self.start_time
        else:
            return -1

    api_protocol: ActionAPIProtocol = Field(
        ActionAPIProtocol.UNDEFINED,
        description='API Procotol',
    )

    # To be set by Adapter, not by user
    state: ActionState = Field(
        ActionState.PENDING,
        description='Action State',
    )
    input: BaseActionInputModel = Field(
        BaseActionInputModel(),
        description='Action Input',
    )
    output: BaseActionOutputModel = Field(
        BaseActionOutputModel(),
        description='Action Output',
    )
    response_status: OtherResponseStatusEnum = Field(
        OtherResponseStatusEnum.UNITIALISED_STATUS,
        description='Actual Response Status',
    )

    exec: Optional[str] = Field(
        None,
        description='Exception Message when Action is in Error State'
    )


class JsonHttpActionModel(BaseActionModel):
    config: JsonHttpActionConfigModel = Field(
        JsonHttpActionConfigModel(),
        description=BaseActionModel.model_fields['config'].description,
    )
    api_protocol: ActionAPIProtocol = Field(
        ActionAPIProtocol.HTTP,
        description=BaseActionModel.model_fields['api_protocol'].description,
    )

    input: JsonHttpActionInputModel = Field(
        JsonHttpActionInputModel(),
        description=BaseActionModel.model_fields['input'].description,
    )
    output: JsonHttpActionOutputModel = Field(
        JsonHttpActionOutputModel(),
        description=BaseActionModel.model_fields['output'].description,
    )
    response_status: Union[HttpResponseStatusEnum, OtherResponseStatusEnum] = Field(
        OtherResponseStatusEnum.UNITIALISED_STATUS,
        description=BaseActionModel.model_fields['response_status'].description,
    )


class JsonRpcWebSocketActionModel(BaseActionModel):
    config: JsonRpcWebSocketActionConfigModel = Field(
        JsonRpcWebSocketActionConfigModel(),
        description=BaseActionModel.model_fields['config'].description,

    )
    api_protocol: ActionAPIProtocol = Field(
        ActionAPIProtocol.WEBSOCKET,
        description=BaseActionModel.model_fields['api_protocol'].description,

    )

    input: JsonRpcWebSocketActionInputModel = Field(
        JsonRpcWebSocketActionInputModel(),
        description=BaseActionModel.model_fields['input'].description,
    )
    output: JsonRpcWebSocketActionOutputModel = Field(
        JsonRpcWebSocketActionOutputModel(),
        description=BaseActionModel.model_fields['output'].description,
    )
    response_status: Union[WebSocketResponseStatusEnum, OtherResponseStatusEnum] = Field(
        OtherResponseStatusEnum.UNITIALISED_STATUS,
        description=BaseActionModel.model_fields['response_status'].description,
    )
