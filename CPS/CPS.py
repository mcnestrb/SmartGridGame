import sys
from twisted.python import log
from twisted.internet import reactor

from CPSFactory import CPSFactory

PORT = 9000

if __name__ == '__main__':
    log.startLogging(sys.stdout)
    log.msg("Running Server")
    count = int(sys.argv[1])
    factory = CPSFactory(count)
    reactor.listenTCP(PORT, factory)
    reactor.run()
