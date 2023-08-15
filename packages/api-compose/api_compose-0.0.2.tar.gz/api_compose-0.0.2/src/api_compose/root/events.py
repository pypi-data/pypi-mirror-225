from api_compose.core.events.base import BaseEvent, BaseData, EventType


class SessionEvent(BaseEvent):
    event: EventType = EventType.Session
    data: BaseData = BaseData()
