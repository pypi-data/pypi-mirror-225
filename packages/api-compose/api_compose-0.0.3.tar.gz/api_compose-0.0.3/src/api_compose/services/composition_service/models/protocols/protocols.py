from enum import Enum


class ActionAPIProtocol(str, Enum):
    """
    Action State as determined by the executor
    """

    UNDEFINED = 'undefined'
    HTTP = 'http'
    WEBSOCKET = 'websocket'
    GRPC = 'grpc'
    FIX = 'fix'
