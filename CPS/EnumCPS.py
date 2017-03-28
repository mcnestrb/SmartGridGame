from enum import Enum

class CPSState(Enum):
    IDLE = 1
    START = 2
    INIT = 3
    GAME = 4
    OPT = 5
    DISTRIBUTE = 6
