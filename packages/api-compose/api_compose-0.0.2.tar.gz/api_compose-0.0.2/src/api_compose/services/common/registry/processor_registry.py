from enum import Enum
from typing import Type, Callable, List, Optional, Dict, Generator

from pydantic import BaseModel as _BaseModel
from pydantic import Field

from api_compose.core.logging import get_logger
from api_compose.services.common.events.controller_registration import ProcessorRegistrationData, \
    ProcessorRegistrationEvent
from api_compose.services.common.models.base import BaseModel
from api_compose.services.common.processors.base import BaseProcessor, BaseProcessorSubclass

logger = get_logger(__name__)


class ProcessorType(str, Enum):
    Builtin = 'Builtin'
    Custom = 'Custom'


class PrceossorCategory(str, Enum):
    Action = 'Action'
    Adapter = 'Adapter'
    Executor = 'Executor'
    Backend = 'Backend'
    Assertion = 'Assertion'
    Reporting = 'Reporting'

    # for testing only
    _Unknown = 'Unknown'


class ProcessorRegistryEntry(_BaseModel, extra='forbid'):
    clazz: Type[BaseProcessor]
    category: PrceossorCategory = Field(description='Category the asset belongs to')
    type: ProcessorType
    models: List[BaseModel] = Field(description='Example Models')

    @property
    def class_name(self):
        return self.clazz.__qualname__.split('.')[-1]


class ProcessorRegistry:
    """
    Applied on Class
    """
    registry: List[ProcessorRegistryEntry] = []

    @classmethod
    def _validate_no_entry_with_same_class(cls, clazz: Type):
        registered_entry_models = [entry for entry in cls.registry if entry.clazz == clazz]
        assert len(registered_entry_models) == 0, f'The Model Id {clazz} has already been used!'

    @classmethod
    def set(cls,
            models: List[BaseModel],
            processor_category: PrceossorCategory,
            processor_type: ProcessorType = ProcessorType.Custom
            ) -> Callable:

        def decorator(processor_class: Type[BaseProcessor]):
            cls._validate_no_entry_with_same_class(clazz=processor_class)

            cls.registry.append(
                ProcessorRegistryEntry(
                    clazz=processor_class,
                    type=processor_type,
                    category=processor_category,
                    models=models
                )
            )

            logger.info("Registered processor_class=%s" % (processor_class),
                        ProcessorRegistrationEvent(data=ProcessorRegistrationData(processor_class=processor_class)))
            return processor_class

        return decorator


    @classmethod
    def create_processor_by_name(cls, class_name: str, config: Dict) -> BaseProcessorSubclass:
        processor_class: Optional[Type[BaseProcessor]] = None
        for entry in cls.registry:
            if entry.class_name == class_name:
                processor_class = entry.clazz

        if processor_class is None:
            raise KeyError(
                f'No controller is found with {class_name=}. Registered controller names are {[entry.class_name for entry in cls.registry]}')
        else:
            return processor_class(**config)

    @classmethod
    def create_model_by_name(cls, model_name: str, config: Dict) -> BaseModel:
        available_models = []
        model = None
        for candidate_model in cls.get_models():
            candidate_model_name = candidate_model.__class__.__name__
            available_models.append(candidate_model_name)
            if candidate_model_name == model_name:
                model = candidate_model.__class__(**config)

        if model is None:
            raise KeyError(f'No model is found with {model_name=}. {available_models=}')
        else:
            return model

    @classmethod
    def get_model_names(cls) -> Generator[str, str, None]:
        for model in cls.get_models():
            yield model.__class__.__name__

    @classmethod
    def get_models(cls) -> Generator[BaseModel, BaseModel, None]:
        for entry in cls.registry:
            for candidate_model in entry.models:
                yield candidate_model
