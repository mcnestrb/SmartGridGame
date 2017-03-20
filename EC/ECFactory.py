from twisted.internet.protocol import ClientFactory
from twisted.python import log

import ECFSM as FSM
from EnumEC import ECState as state

from ECProtocol import ECProtocol

class ECFactory(ClientFactory):
    def __init__(self):
        self.energy = 0
        self.state = state.NOT_CONNECTED

    def startedConnecting(self, connector):
        log.msg('Started to connect...')

    def buildProtocol(self, addr):
        log.msg('Connected')
        return ECProtocol(self)

    def ECConnectionLost(self, connector, reason):
        log.msg('Lost connection because: {}'.format(reason))

    def ECConnectionFailed(self, connector, reason):
        log.msg('Connection failed because {}'.format(reason))
