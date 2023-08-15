__all__ = [
    "BaseReportRenderer",
]
import datetime
from abc import ABC, abstractmethod
from pathlib import Path

from api_compose.services.common.processors.base import BaseProcessor
from api_compose.services.common.models.base import BaseModel
from api_compose.services.common.registry.processor_registry import ProcessorRegistry
from api_compose.core.logging import get_logger


logger = get_logger(name=__name__)


class BaseReportRenderer(BaseProcessor, ABC):
    """
    Base Class which defines how reports are rendered
    """

    def __init__(
        self,
        model: BaseModel,
        model_template_path: str,
        registry: ProcessorRegistry,
        output_folder: str,
        timestamp: datetime.datetime,
        **kwargs,
    ):
        super().__init__()
        self.model = model
        self.model_template_path = model_template_path
        self.timestamp = timestamp
        self.output_folder_path = Path(output_folder).joinpath(timestamp.isoformat())
        self.output_folder_path.mkdir(parents=True, exist_ok=True)
        self.registry = registry

    def run(self):
        self.render()
        self.write()
        logger.info(f"Report is written to folder={self.output_folder_path.absolute()}")

    @abstractmethod
    def render(self):
        """
        :return:
        """
        pass


    @abstractmethod
    def write(self):
        pass


