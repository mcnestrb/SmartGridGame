import CPSProtocol
from EnumCPS import CPSState as state

from twisted.internet.protocol import ServerFactory

class CPSFactory(ServerFactory):
    def __init__(self):
        self.state = IDLE
        self.ECs = []
        self.suppliers = {}
        self.bidders = {}

    def buildProtocol(self, addr):
        return CPSProtocol(self)
