import sys
from twisted.python import log
from twisted.internet import reactor

from ECFactory import ECFactory

HOST = 'localhost'
PORT = 9000

if __name__ == '__main__':
    log.startLogging(sys.stdout)
    log.msg("Running Client")
    factory = ECFactory()
    reactor.connectTCP(HOST, PORT, factory)

    reactor.run()
