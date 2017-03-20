from twisted.python import log
from twisted.internet.protocol import Protocol

from ECFSM import ECFSM as FSM
from EnumEC import ECState as state

class ECProtocol(Protocol):
    def __init__(self, factory):
        self.factory = factory
        self.FSM = FSM(self)

    def connectionMade(self):
        self.factory.state = state.IDLE

    def dataReceived(self, data):
        if (self.factory.state == state.IDLE):
            self.FSM.idleState(data)
        elif (self.factory.state == state.DEMAND):
            self.FSM.demandState()
        elif (self.factory.state == state.SUPPLY):
            self.FSM.supplyState()
        elif (self.factory.state == state.EST_1):
            self.FSM.est1State()
        elif (self.factory.state == state.EST_2):
            self.FSM.est2State()
        elif (self.factory.state == state.RECEIVE):
            self.FSM.receiveState()

    def connectionLost(self, reason):
        log.msg('Lost connection because {}'.format(reason))
