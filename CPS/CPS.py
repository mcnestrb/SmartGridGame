import sys
from twisted.python import log
from twisted.internet import reactor
from twisted.internet.protocol import ServerFactory, ClientFactory, Protocol
from EnumCPS import CPSState as state
import CPSFSM as FSM


PORT = 9000

class CPS(Protocol):
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

class CPSFactory(ServerFactory):
    def __init__(self):
        self.state = IDLE
        self.ECs = []
        self.suppliers = {}
        self.bidders = {}

    def buildProtocol(self, addr):
        return CPS(self)

if __name__ == '__main__':
    log.startLogging(sys.stdout)
    log.msg("Running Server")
    factory = CPSFactory()
    reactor.listenTCP(PORT, factory)
    reactor.run()
