from enum import Enum

class ECState(Enum):
    NOT_CONNECTED = 0
    IDLE = 1
    START = 2
    DEMAND = 3
    SUPPLY = 4
    EST_1 = 5
    EST_2 = 6
    RECEIVE = 7
