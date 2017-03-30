from CPSProtocol import CPSProtocol
from EnumCPS import CPSState as state
from collections import OrderedDict

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
        self.pricePerUnit = 0
        self.P = 0.0
        self.pn_max = 0.0
        self.pn_min = 8.50
        self.initPrice = 0
        self.offers = {}
        self.prices = OrderedDict()

    def buildProtocol(self, addr):
        return CPSProtocol(self)
