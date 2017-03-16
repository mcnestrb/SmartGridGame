from twisted.internet.protocol import Protocol
from twisted.python import log

import CPSFSM as FSM
from EnumCPS import CPSState as state

class CPSProtocol(Protocol):
    def __init__(self, factory):
        self.factory = factory
        self.FSM = FSM(self)

    def connectionMade(self):
        peer = self.transport.getPeer()
        log.msg('Client connection from {}'.format(peer))
        self.factory.ECs.append(peer)
        log.msg('All connection {}'.format(self.factory.ECs))

    def dataReceived(self, data):
        if (self.factory.state == state.IDLE):
            self.FSM.
        elif (self.factory.state == state.START):
        elif (self.factory.state == state.INIT):
        elif (self.factory.state == state.OPT):
        elif (self.factory.state == state.DISTRIBUTE):

    def connectionLost(self, reason):
        log.msg('Lost connection because {}'.format(reason))
