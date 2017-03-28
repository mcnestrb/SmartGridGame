from CPSProtocol import CPSProtocol
from EnumCPS import CPSState as state

from twisted.internet.protocol import ServerFactory

class CPSFactory(ServerFactory):
    def __init__(self):
        self.state = state.IDLE
        self.ECs = {}
        self.suppliers = {}
        self.bidders = {}
        self.absent = {}
        self.Edef = 0
        self.N = 0
        self.P = 0
        self.offers = {}

    def buildProtocol(self, addr):
        return CPSProtocol(self)
