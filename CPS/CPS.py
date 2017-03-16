import sys
from twisted.python import log
from twisted.internet import reactor
from twisted.internet.protocol import ServerFactory, ClientFactory, Protocol

import CPSFactory

PORT = 9000

if __name__ == '__main__':
    log.startLogging(sys.stdout)
    log.msg("Running Server")
    factory = CPSFactory()
    reactor.listenTCP(PORT, factory)
    reactor.run()
