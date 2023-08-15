from api_compose.core.events.base import BaseEvent, BaseData, EventType


class CliEvent(BaseEvent):
    event: EventType = EventType.CLI
    data: BaseData = BaseData()
