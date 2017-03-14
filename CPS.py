import sys
from twisted.python import log
from twisted.internet import reactor
from twisted.internet.protocol import ServerFactory, ClientFactory, Protocol

PORT = 9000

class CPS(Protocol):
    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        log.msg('Client connection from {}'.format(self.transport.getPeer()))

    def dataReceived(self, data):
        log.msg('Data received {}'.format(data))
        if( self.factory.state == 'first'):
            log.msg('Reply as normal')
            self.factory.state = 'second'
            log.msg('{}'.format(self.factory.state))
            self.transport.write(data)
        elif ( self.factory.state == 'second'):
            log.msg('Refuse connection')
            self.factory.state = 'first'
            log.msg('{}'.format(self.factory.state))
            self.transport.write('close'.encode())

    def connectionLost(self, reason):
        log.msg('Lost connection because {}'.format(reason))

class CPSFactory(ServerFactory):
    def __init__(self):
        self.state = 'first'

    def buildProtocol(self, addr):
        return CPS(self)

log.startLogging(sys.stdout)
log.msg("Running Server")
factory = CPSFactory()
reactor.listenTCP(PORT, factory)
reactor.run()
