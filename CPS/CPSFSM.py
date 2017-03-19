from twisted.python import log
from EnumCPS import CPSState as state

class CPSFSM():
    def __init__(self, protocol):
        self.protocol = protocol

    def idleState(data, peer):
        energy = int(data)
        if (peer in self.protocol.factory.ECs):
            if ( energy > 0 ):
                self.protocol.factory.suppliers.update({peer: energy})
            elif (energy < 0):
                self.protocol.factory.bidders.update({peer: energy})
            else:
                self.protocol.factory.absent.append(peer)
        else:
            log.msg('Error peer not connected')

        bidders = self.protocol.factory.bidders
        suppliers = self.protocol.factory.suppliers
        absent = self.protocol.factory.absent
        ECs = self.protocol.factory.ECs
        if (len(ECs) == len(bidders) + len(suppliers) + len(absent)):
            log.msg('Moving from IDLE to START')
            self.protocol.factory.state = state.START


    def startState():
        log.msg('Moving from START to INIT')
        self.protocol.factory.state = state.INIT

    def initState():
        log.msg('Moving from INIT to OPT')
        self.protocol.factory.state = state.OPT

    def optState():
        log.msg('Moving from OPT to DISTRIBUTE')
        self.protocol.factory.state = state.DISTRIBUTE

    def distributeState():
        log.msg('Moving from DISTRIBUTE to IDLE')
        self.protocol.factory.state = state.IDLE
