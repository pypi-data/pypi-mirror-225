from enum import Enum


class ActionState(str, Enum):
    """
    Action State as determined by the executor
    """

    PENDING = "pending"
    STARTED = "started"
    RUNNING = "running"
    ERROR = "error"
    ENDED = "ended"

    # Reason for discarding: i. upstream action failed.
    DISCARDED = "discarded"
