__all__ = ['BaseAssertion']

from abc import ABC, abstractmethod

from api_compose.services.common.processors.base import BaseProcessor
from api_compose.services.assertion_service.models.assertion import BaseAssertionModel, AssertionState


class BaseAssertion(BaseProcessor, ABC):

    def __init__(self,
                 assertion: BaseAssertionModel,
                 *args,
                 **kwargs
                 ):
        super().__init__(*args, **kwargs)
        self.assertion = assertion

    def run(self):
        try:
            is_success = self.execute()
            exec = None
        except Exception as e:
            is_success = False
            exec = str(e)

        self.assertion.is_success = is_success
        self.assertion.exec = exec
        self.assertion.state = AssertionState.EXECUTED


    @abstractmethod
    def execute(self) -> bool:
        pass