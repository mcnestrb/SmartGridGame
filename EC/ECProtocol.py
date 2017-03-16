from twisted.python import log
from twisted.internet.protocol import Protocol

import ECFSM as FSM
from EnumEC import ECState as state

class ECProtocol(Protocol):
    def __init__(self, factory):
        self.factory = factory
        self.FSM = FSM(self)

    def connectionMade(self):
        self.factory.state = state.IDLE

    def dataReceived(self, data):
        if (self.factory.state == state.IDLE):
        elif (self.factory.state == state.DEMAND):
        elif (self.factory.state == state.SUPPLY):
        elif (self.factory.state == state.EST_1):
        elif (self.factory.state == state.EST_2):
        elif (self.factory.state == state.RECEIVE):

    def connectionLost(self, reason):
        log.msg('Lost connection because {}'.format(reason))
