from pydantic import ConfigDict, BaseModel as _BaseModel
from enum import Enum

class EventType(Enum):
    # Registration
    ProcessorRegistration = 'ProcessorRegistration'
    CalculateFieldRegistration = 'CalculatedFieldRegistration'

    # Others
    Action = 'Action'
    Default = 'Default'
    Scheduler = 'Scheduler'
    CalculateFieldRendering = 'CalculatedFieldRendering'
    ReadConfiguration = 'ReadConfiguration'
    TemplatedField = 'TemplatedField'
    Deserialisation = 'Deserialisation'
    Session = 'Session'
    CLI = 'Cli'

    def __json__(self):
        return self.value





class BaseData(_BaseModel):
    model_config = ConfigDict(extra="allow")



class BaseEvent(_BaseModel):
    event: EventType
    data: BaseData
