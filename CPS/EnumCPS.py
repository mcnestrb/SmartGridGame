from enum import Enum

class CPSState(Enum):
    IDLE = 1
    START = 2
    INIT = 3
    GAME_1 = 4
    OPT = 5
    GAME_2 = 6
    DISTRIBUTE = 7
