from typing import List, Any

import networkx as nx
from networkx.readwrite import json_graph
from pydantic import BaseModel as _BaseModel, ConfigDict, field_serializer, field_validator
from pydantic import Field

from api_compose.core.logging import get_logger
from api_compose.services.assertion_service.models.assertion import BaseAssertionModel
from api_compose.services.common.models.base import BaseModel
from api_compose.services.composition_service.models.actions.actions import BaseActionModel
from api_compose.services.composition_service.models.actions.states import ActionState
from api_compose.services.composition_service.models.executors.configs import BaseExecutorConfigModel, \
    LocalExecutorConfigModel
from api_compose.services.composition_service.models.executors.enum import ExecutorProcessorEnum
from api_compose.services.composition_service.models.schedulers.configs import ActionSchedulerConfigModel

logger = get_logger(__name__)


class ScenarioModelConfig(_BaseModel):
    executor: ExecutorProcessorEnum = Field(
        ExecutorProcessorEnum.LocalExecutor,
        description='Executor Implementation to use',
    )
    executor_config: BaseExecutorConfigModel = Field(
        LocalExecutorConfigModel(),
        description='Config required by Executor Implementation',
    )

    scheduler_config: ActionSchedulerConfigModel = Field(
        ActionSchedulerConfigModel(),
        description='Config required by the Action Scheduler',
    )

    enable_data_type_checking: bool = Field(
        False,
        description='Whether to enable data type checking for each Action in this scenario'
    )


class ScenarioModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    config: ScenarioModelConfig = ScenarioModelConfig()
    actions: List[BaseActionModel]

    assertions: List[BaseAssertionModel] = []

    digraph: nx.DiGraph = Field(
        nx.DiGraph(),
    )

    @field_validator("actions", "assertions", mode="before")
    @classmethod
    def parse_input(cls, value: Any):
        """
        Create Actions and Assertions with the appropriate Model Type
        """
        from api_compose.services.common.registry.processor_registry import ProcessorRegistry
        list_ = []
        if type(value) == list:
            for val in value:
                if type(val) == dict:
                    # if dict, deserialise it to model
                    model = ProcessorRegistry.create_model_by_name(val.get('model_name'), val)
                    list_.append(model)
                else:
                    # Keep the original model
                    list_.append(val)
        else:
            logger.warning(f'Must be a list. Received {value=}')

        return list_

    @field_serializer('digraph')
    def serialize_digraph(self, digraph: nx.DiGraph, _info):
        return json_graph.node_link_data(digraph)

    @property
    def digraph_file_name(self) -> str:
        return self.fqn.replace('.', '-') + '.png'

    start_time: float = Field(
        -1,
        description='Start Time, number of seconds passed since epoch',

    )
    end_time: float = Field(
        -1,
        description='End Time, number of seconds passed since epoch',

    )

    @property
    def is_success(self):
        return (all(assertion_item.is_success for assertion_item in self.assertions)
                and all(action.state == ActionState.ENDED for action in self.actions))

    @property
    def elapsed_time(self) -> float:
        if self.start_time > 0 and self.end_time > 0:
            return self.end_time - self.start_time
        else:
            return -1
