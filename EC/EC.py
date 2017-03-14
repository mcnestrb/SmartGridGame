import sys
from twisted.python import log
from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory, Protocol

from EnumEC import ECState as state
import ECFSM as FSM

HOST = 'localhost'
PORT = 9000

class EC(Protocol):
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

class ECFactory(ClientFactory):
    def __init__(self, energy):
        self.energy = energy
        self.state = ECState.NOT_CONNECTED

    def startedConnecting(self, connector):
        log.msg('Started to connect...')

    def buildProtocol(self, addr):
        log.msg('Connected')
        return EC(self)

    def ECConnectionLost(self, connector, reason):
        log.msg('Lost connection because: {}'.format(reason))

    def ECConnectionFailed(self, connector, reason):
        log.msg('Connection failed because {}'.format(reason))

if __name__ == '__main__':
    energy = sys.argv[1]
    log.startLogging(sys.stdout)
    log.msg("Running Client")
    factory = ECFactory(energy)
    reactor.connectTCP(HOST, PORT, factory)

    reactor.run()
