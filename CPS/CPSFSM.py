from twisted.python import log
from EnumCPS import CPSState as state

class CPSFSM():
    def __init__(self, protocol):
        self.protocol = protocol

    def idleState(self):
        start = input('Do you want to start? y/n\n')
        if (start == 'y'):
            log.msg('Moving from IDLE to START')
            self.protocol.factory.state = state.START
            data = 'Timeslot: {}'.format(14)
            for EC in list(self.protocol.factory.ECs):
                self.protocol.factory.ECs[EC].transport.write(data.encode())

    def startState(self, data, peer):
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

        # if all connected ECs have declared their energy then the game begins
        bidders = self.protocol.factory.bidders
        suppliers = self.protocol.factory.suppliers
        absent = self.protocol.factory.absent
        ECs = self.protocol.factory.ECs
        if (len(ECs) == len(bidders) + len(suppliers) + len(absent)):
            log.msg('All bidders: {}'.format(bidders))
            log.msg('All suppliers: {}'.format(suppliers))
            log.msg('Moving from START to INIT')
            self.protocol.factory.state = state.INIT

            Edef = 0
            for key in bidders:
                Edef -= bidders[key]
            N = len(suppliers)
            self.protocol.factory.Edef = Edef
            self.initState()

    def initState(self):
        self.protocol.factory.P = 10
        log.msg('P:{}'.format(self.protocol.factory.P))
        log.msg('Edef:{}'.format(self.protocol.factory.Edef))
        log.msg('N:{}'.format(self.protocol.factory.N))

        data = 'P: %s, Edef: %s, N: %s' % (self.protocol.factory.P, self.protocol.factory.Edef, self.protocol.factory.N)

        for supplier in list(self.protocol.factory.suppliers):
            self.protocol.factory.ECs[supplier].transport.write(data.encode())

        log.msg('Moving from INIT to OPT')
        self.protocol.factory.state = state.OPT

    def optState(self, data, peer):
        offer = float(data.decode())
        self.protocol.factory.offers[peer] = offer
        if ( len(self.protocol.factory.offers) == len(self.protocol.factory.suppliers) ):
            total_offer = 0
            for key in self.protocol.factory.offers:
                total_offer += self.protocol.factory.offers[key]
            if (total_offer >= self.protocol.factory.Edef):
                # DO THE OPT THINGY
                log.msg('Moving from OPT to DISTRIBUTE')
                self.protocol.factory.state = state.DISTRIBUTE
            else:
                data = 'P: %s, Edef: %s, N: %s' % (self.protocol.factory.P, self.protocol.factory.Edef, self.protocol.factory.N)

                for supplier in list(self.protocol.factory.suppliers):
                    self.protocol.factory.ECs[supplier].transport.write(data.encode())

                log.msg('Staying in OPT state')

    def distributeState(self):
        log.msg('Moving from DISTRIBUTE to IDLE')
        self.protocol.factory.state = state.IDLE
