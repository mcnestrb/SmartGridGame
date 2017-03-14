from enum import Enum

class ECState(Enum):
    NOT_CONNECTED = 0
    IDLE = 1
    DEMAND = 2
    SUPPLY = 3
    EST_1 = 4
    EST_2 = 5
