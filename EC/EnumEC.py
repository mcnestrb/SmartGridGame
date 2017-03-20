from enum import Enum

class ECState(Enum):
    NOT_CONNECTED = 0
    IDLE = 1
    START = 2
    EST_1 = 3
    EST_2 = 4
    RECEIVE = 5
