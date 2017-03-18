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
            elif: (energy < 0):
                self.protocol.factory.bidders.update({peer: energy})
        else:
            log.msg('Error peer not connected')

    def startState():
        log.msg('Moving from START to INIT')
        self.protocol.factory.state = state.IDLE

    def initState():
        log.msg('Moving from INIT to OPT')
        self.protocol.factory.state = state.OPT

    def optState():
        log.msg('Moving from OPT to DISTRIBUTE')
        self.protocol.factory.state = state.DISTRIBUTE

    def distributeState():
        log.msg('Moving from DISTRIBUTE to IDLE')
        self.protocol.factory.state = state.IDLE
