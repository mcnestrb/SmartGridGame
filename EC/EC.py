import sys
from twisted.python import log
from twisted.internet import reactor

from ECFactory import ECFactory

HOST = 'localhost'
PORT = 9000

if __name__ == '__main__':
    log.startLogging(sys.stdout)
    log.msg("Running Client")
    dummy = True
    energy = -10
    with open(sys.argv[1]) as fp:
        for i, line in enumerate(fp):
            if i == int(sys.argv[2]):
                energy = int(line)
                if (sys.argv[2] == 0):
                    energy *= -1

    factory = ECFactory(energy)
    reactor.connectTCP(HOST, PORT, factory)
    reactor.run()
