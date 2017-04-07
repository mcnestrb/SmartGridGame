from EnumCPS import CPSState as state

import numpy as np
from cvxpy import *

from twisted.python import log

from collections import OrderedDict

class CPSFSM():
    def __init__(self, protocol):
        self.protocol = protocol

    def idleState(self):
        if(self.protocol.factory.count == len(self.protocol.factory.ECs)):
            start = input('All {} ECs are in the network\nDo you want to start?\n'.format(self.protocol.factory.count))
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
            self.protocol.factory.N = len(suppliers)
            self.protocol.factory.Edef = Edef
            self.initState()

    def initState(self):
        self.protocol.factory.pricePerUnit = 1.85
        log.msg('Price per Unit: {}'.format(self.protocol.factory.pricePerUnit))
        log.msg('Edef: {}'.format(self.protocol.factory.Edef))
        log.msg('N: {}'.format(self.protocol.factory.N))

        self.protocol.factory.P = self.protocol.factory.Edef * self.protocol.factory.pricePerUnit
        self.protocol.factory.pn_max = self.protocol.factory.P
        self.protocol.factory.initPrice = self.protocol.factory.P / self.protocol.factory.N


        data = 'Initial - Price: %s, Edef: %s' % (self.protocol.factory.initPrice, self.protocol.factory.Edef)

        for supplier in list(self.protocol.factory.suppliers):
            self.protocol.factory.prices[supplier] = self.protocol.factory.initPrice
            self.protocol.factory.ECs[supplier].transport.write(data.encode())

        log.msg('Moving from INIT to GAME_1')
        self.protocol.factory.state = state.GAME_1

    def game1State(self, data, peer):
        offer = float(data.decode())
        self.protocol.factory.offers[peer] = offer
        if ( len(self.protocol.factory.offers) == len(self.protocol.factory.suppliers) ):
            log.msg('Slack Vars: {}'.format(self.protocol.factory.offers))
            ve = True
            keys = list(self.protocol.factory.offers.keys())
            curr_slack_var = self.protocol.factory.offers[keys[0]]
            for key in keys[1:]:
                if(curr_slack_var != self.protocol.factory.offers[key]):
                    ve = False
            if (ve):
                log.msg('Moving from GAME_1 to OPT')
                self.protocol.factory.state = state.OPT
                data = 'End'
            else:
                log.msg('Staying in GAME_1 state')
                data = 'Price: %s, Edef: %s' % (self.protocol.factory.initPrice, self.protocol.factory.Edef)

            for supplier in list(self.protocol.factory.suppliers):
                self.protocol.factory.ECs[supplier].transport.write(data.encode())

            self.protocol.factory.offers = {}

    def optState(self, data, peer):
        offer = float(data.decode())
        self.protocol.factory.offers[peer] = offer
        if ( len(self.protocol.factory.offers) == len(self.protocol.factory.suppliers) ):
            # Convex Optimisation
            log.msg('Offers: {}'.format(self.protocol.factory.offers))

            pn = Variable( len(self.protocol.factory.offers) )

            # Get energy offers after first game and add them to a numpy array
            arr = [self.protocol.factory.offers[offer] for offer in self.protocol.factory.offers]
            log.msg('Array of offers: {}'.format(arr))
            en = np.array(arr)
            r = 2
            a = 1
            b = 1

            pn_min = self.protocol.factory.pn_min
            pn_max = self.protocol.factory.pn_max
            constraints = [pn_min <= pn, pn <= pn_max, sum_entries(pn) == self.protocol.factory.P]

            objective = Minimize(sum_entries( (en * (pn ** r)) + (a * pn) + b ) )

            problem = Problem(objective, constraints)
            problem.solve()
            p_star = self.flatten_p_star(pn.value)

            log.msg('P STAR: {}'.format(p_star))
            log.msg('FIRST: {}'.format(p_star[0]))
            log.msg('SECOND: {}'.format(p_star[1]))

            i = 0
            for key in self.protocol.factory.prices:
                self.protocol.factory.prices[key] = p_star[i]
                i += 1

            log.msg('Moving from OPT to GAME_2')
            self.protocol.factory.state = state.GAME_2
            self.protocol.factory.offers = {}
            for supplier in list(self.protocol.factory.suppliers):
                data = 'Updated price: {}'.format(self.protocol.factory.prices[supplier])
                self.protocol.factory.ECs[supplier].transport.write(data.encode())

    def game2State(self, data, peer):
        log.msg('Offer: {}'.format(data))
        offer = float(data.decode())
        self.protocol.factory.offers[peer] = offer
        if ( len(self.protocol.factory.offers) == len(self.protocol.factory.suppliers) ):
            log.msg('Slack Vars: {}'.format(self.protocol.factory.offers))
            ve = True
            keys = list(self.protocol.factory.offers.keys())
            curr_slack_var = self.protocol.factory.offers[keys[0]]
            for key in keys[1:]:
                if(curr_slack_var != self.protocol.factory.offers[key]):
                    ve = False

            if (ve):
                log.msg('Moving from GAME_2 to DISTRIBUTE')
                self.protocol.factory.state = state.DISTRIBUTE
                data = 'End'
                for supplier in list(self.protocol.factory.suppliers):
                    self.protocol.factory.ECs[supplier].transport.write(data.encode())
            else:
                log.msg('Staying in GAME_2 state')
                for supplier in list(self.protocol.factory.suppliers):
                    data = 'Price: %s' % (self.protocol.factory.prices[supplier])
                    self.protocol.factory.ECs[supplier].transport.write(data.encode())


            self.protocol.factory.offers = {}

    def distributeState(self, data, peer):
        offer = float(data.decode())
        self.protocol.factory.offers[peer] = offer
        if ( len(self.protocol.factory.offers) == len(self.protocol.factory.suppliers) ):
            log.msg('Offers: {}'.format(self.protocol.factory.offers))
            total_energy = sum(self.protocol.factory.offers.values())
            log.msg('Need to buy {} kWh of energy from the central grid'.format(self.protocol.factory.Edef - total_energy))

            log.msg('Moving from DISTRIBUTE to IDLE')
            self.protocol.factory.state = state.IDLE
            for bidder in list(self.protocol.factory.bidders):
                data = str(self.protocol.factory.bidders[bidder])
                self.protocol.factory.ECs[bidder].transport.write(data.encode())

    def flatten_p_star(self, p_star):
        temp_list = p_star.flatten().tolist()
        return [item for sublist in temp_list for item in sublist]
