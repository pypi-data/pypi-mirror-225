from __future__ import annotations

__all__ = ["BaseAdapter"]

import time
import traceback
from abc import ABC, abstractmethod
from typing import Dict, Union, List
from xml.dom.minidom import Element

from api_compose import GlobalSettings
from api_compose.core.jinja.core.engine import JinjaEngine
from api_compose.core.logging import get_logger
from api_compose.services.common.processors.base import BaseProcessor
from api_compose.services.common.templated_field.templated_field import BaseTemplatedTextField
from api_compose.services.composition_service.events.action import ActionData, ActionEvent
from api_compose.services.composition_service.jinja.context import ActionJinjaContext
from api_compose.services.composition_service.models.actions.actions import BaseActionModel
from api_compose.services.composition_service.models.actions.inputs import BaseActionInputModel
from api_compose.services.composition_service.models.actions.outputs import BaseActionOutputModel
from api_compose.services.composition_service.models.actions.states import ActionState
from api_compose.services.composition_service.models.calculated_field.calculated_field import CalculatedField, \
    BuiltinCalculatedFieldNameEnum, get_calculated_fields_in_string
from api_compose.services.composition_service.models.protocols.hints import ResponseStatusEnum
from api_compose.services.composition_service.models.protocols.status_enums import OtherResponseStatusEnum
from api_compose.services.composition_service.registry.calculated_field_registry import CalculatedFieldRegistry
from api_compose.services.persistence_service.processors.base_backend import BaseBackend

logger = get_logger(name=__name__)


class BaseAdapter(BaseProcessor, ABC):
    """
    Network Communication
    """

    OUTPUT_BODY_KEY = 'message'
    DEBUG_OUTPUT_BODY: str = ""
    ERROR_OUTPUT_BODY: str = ""

    @CalculatedFieldRegistry.set(name=BuiltinCalculatedFieldNameEnum.URL.value)
    def calculate_url(self, **ctx):
        return self.url.render(jinja_engine=self.jinja_engine, jinja_context=self.jinja_context).load().loaded

    def __init__(
            self,
            action_model: BaseActionModel,
            url: BaseTemplatedTextField,
            jinja_engine: JinjaEngine,
            backend: BaseBackend,
            **kwargs,
    ):
        super().__init__(**kwargs)
        self.url: BaseTemplatedTextField = url
        self.backend = backend
        self.action_model = action_model

        # values to be set
        self.required_templated_fields: Dict[str, BaseTemplatedTextField] = {BuiltinCalculatedFieldNameEnum.URL.value: self.url}
        self.calculated_field_registry = CalculatedFieldRegistry()

        self.jinja_engine: JinjaEngine = jinja_engine

        self.input: BaseActionInputModel = BaseActionInputModel()
        self.output: BaseActionOutputModel = BaseActionOutputModel()
        self.response_status: ResponseStatusEnum = (
            OtherResponseStatusEnum.UNITIALISED_STATUS
        )

        # Initialise state
        state = ActionState.PENDING
        logger.info(f"Action %s is in state %s" % (self.action_model.execution_id, state),
                    ActionEvent(data=ActionData(id=self.action_model.execution_id, state=state)))
        self.action_model.state = state

    @abstractmethod
    def _on_start(self, is_debug: bool, jinja_context: ActionJinjaContext):
        """
        Hook before calling self.on_exchange().
        :return:
        """
        self.jinja_context: ActionJinjaContext = jinja_context

        # CalculatedFieldRegistry.reset()
        state = ActionState.STARTED
        self.action_model.start_time = time.time()

        logger.info(f"Action %s is in state %s" % (self.action_model.execution_id, state),
                    ActionEvent(data=ActionData(id=self.action_model.execution_id, state=state)))
        self.action_model.state = state

        for name, templated_field in self.required_templated_fields.items():
            self.calculated_field_registry.set_attrs_by_name(name,
                                                             get_calculated_fields_in_string(templated_field.template),
                                                             True)

        for val in self.calculated_field_registry.render(
                self,
                self.action_model.execution_id,
                **GlobalSettings.get().env_vars,
        ):
            val: CalculatedField = val
            self.jinja_context.calculated_fields.append(val)

    @abstractmethod
    def _on_exchange(self, is_debug: bool):
        """
        Main method to connect with different systems.

        :return:
        """
        state = ActionState.RUNNING
        logger.info(f"Action %s is in state %s" % (self.action_model.execution_id, state),
                    ActionEvent(data=ActionData(id=self.action_model.execution_id, state=state)))
        self.action_model.state = state

    @abstractmethod
    def _set_response_status(self):
        """
        Set self.status

        Return the status after calling self.connect()
        :return:
        """
        pass

    @abstractmethod
    def _set_input(self):
        """
        Set self.input.

        Return a dictionary of rendered input used in calling self.connect()
        :return:
        """
        pass

    @abstractmethod
    def _set_output(self):
        """
        Set self.output

        Return a dictionary of output from calling self.on_exchange()
        :return:
        """
        pass

    @abstractmethod
    def _on_error(self, is_debug: bool):
        """
        Hook to handle error.
        :return:
        """
        state = ActionState.ERROR
        logger.error(f"Action %s is in state %s" % (self.action_model.execution_id, state),
                    ActionEvent(data=ActionData(id=self.action_model.execution_id, state=state)))
        self.action_model.state = state
        self.action_model.exec = traceback.format_exc()

        # Add current action to database and update core context
        self.backend.add(self.action_model)
        self.jinja_context.action_models.append(self.action_model)

    @abstractmethod
    def _on_end(self, is_debug: bool):
        """
        Hook to postprocess stuff
        :return:
        """
        state = ActionState.ENDED
        self.action_model.end_time = time.time()

        # Clear core context calculated fields
        self.jinja_context.calculated_fields = []

        logger.info(f"Action %s is in state %s" % (self.action_model.execution_id, state),
                    ActionEvent(data=ActionData(id=self.action_model.execution_id, state=state)))
        self.action_model.state = state

        # Add current action to database and update core context
        self.backend.add(self.action_model)
        self.jinja_context.action_models.append(self.action_model)

    @abstractmethod
    def start(self, is_debug: bool, jinja_context: ActionJinjaContext):
        pass

    @abstractmethod
    def stop(self, is_debug: bool):
        pass
