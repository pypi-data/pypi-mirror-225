from api_compose.core.events.base import BaseEvent, BaseData, EventType


class DeserialisationEvent(BaseEvent):
    event: EventType = EventType.Deserialisation
    data: BaseData = BaseData()
