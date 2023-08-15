from api_compose.core.events.base import BaseEvent, BaseData, EventType
from api_compose.services.composition_service.models.actions.states import ActionState


class ActionData(BaseData):
    id: str
    state: ActionState = ActionState.PENDING


class ActionEvent(BaseEvent):
    event: EventType = EventType.Action
    # state:
    data: ActionData
