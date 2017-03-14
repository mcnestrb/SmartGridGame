from enum import Enum

class CPSState(Enum):
    IDLE = 1
    START = 2
    INIT = 3
    OPT = 4
    DISTRIBUTE = 5
