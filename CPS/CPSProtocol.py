from twisted.internet.protocol import Protocol
from twisted.python import log

from CPSFSM import CPSFSM as FSM
from EnumCPS import CPSState as state

class CPSProtocol(Protocol):
    def __init__(self, factory):
        self.factory = factory
        self.FSM = FSM(self)

    def connectionMade(self):
        peer = self.transport.getPeer()
        log.msg('Client connection from {}'.format(peer))
        self.factory.ECs.update({peer: self})
        log.msg('All connections {}'.format(self.factory.ECs))
        self.FSM.idleState()

    def dataReceived(self, data):
        peer = self.transport.getPeer()
        if (self.factory.state == state.START):
            self.FSM.startState(data, peer)
        elif (self.factory.state == state.GAME):
            self.FSM.gameState(data, peer)
        elif (self.factory.state == state.OPT):
            self.FSM.optState(data, peer)
        elif (self.factory.state == state.DISTRIBUTE):
            self.FSM.distributeState()

    def connectionLost(self, reason):
        log.msg('Lost connection because {}'.format(reason))
