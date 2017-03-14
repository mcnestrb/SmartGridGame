import sys
from twisted.python import log
from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory, Protocol

from EnumEC import ECState

HOST = 'localhost'
PORT = 9000

class EC(Protocol):
    def connectionMade(self):
        data = input('\nType a message to send to the CPS\n')
        if (data == 'q'):
            self.transport.loseConnection
        else:
            self.transport.write(data.encode())
            log.msg('Data sent {}'.format(data))

    def dataReceived(self, data):
        log.msg('Data received {}'.format(data))
        if( data == b'close'):
            log.msg('Closing')
            self.transport.loseConnection()
        else:
            data = input('\nType a message to send to the CPS\n')
            if (data == 'q'):
                self.transport.loseConnection
            else:
                self.transport.write(data.encode())
                log.msg('Data sent {}'.format(data))

    def connectionLost(self, reason):
        log.msg('Lost connection because {}'.format(reason))

class ECFactory(ClientFactory):
    def startedConnecting(self, connector):
        log.msg('Started to connect...')

    def buildProtocol(self, addr):
        log.msg('Connected')
        return EC()

    def ECConnectionLost(self, connector, reason):
        log.msg('Lost connection because: {}'.format(reason))

    def ECConnectionFailed(self, connector, reason):
        log.msg('Connection failed because {}'.format(reason))

log.startLogging(sys.stdout)
log.msg("Running Client")
factory = ECFactory()
reactor.connectTCP(HOST, PORT, factory)

reactor.run()
