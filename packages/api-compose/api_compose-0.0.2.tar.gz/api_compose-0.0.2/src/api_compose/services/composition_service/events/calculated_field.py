from typing import Any, List

from api_compose.core.events.base import BaseData, BaseEvent, EventType


class CalculatedFieldData(BaseData):
    name: str
    value: Any
    required: bool
    depends_on: List[str]

class CalculatedFieldRenderingEvent(BaseEvent):
    event: EventType = EventType.CalculateFieldRendering
    # state:
    data: CalculatedFieldData



class CalculatedFieldRegistrationEvent(BaseEvent):
    event: EventType = EventType.CalculateFieldRegistration
    # state:
    data: BaseData() = BaseData()
