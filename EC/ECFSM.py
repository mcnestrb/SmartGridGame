from twisted.python import log
from EnumEC import ECState as state

class ECFSM():
    def __init__(self, protocol):
        self.protocol = protocol

    def idleState(energy):
        if (energy < 0):
            log.msg('Moving from IDLE to DEMAND')
            self.protocol.factory.state = state.DEMAND
            self.protocol.transport.write(energy.encode())
        elif (energy > 0):
            log.msg('Moving from IDLE to SUPPLY')
            self.protocol.factory.state = state.SUPPLY
            self.protocol.transport.write(energy.encode())
        else:
            log.msg('Remain in IDLE state')


    def demandState():
        log.msg('Moving from DEMAND to RECEIVE')
        self.protocol.factory.state = state.RECEIVE

    def supplyState():
        log.msg('Moving from SUPPLY to EST_1')
        self.protocol.factory.state = state.EST_1

    def est1State():
        log.msg('Moving from EST_1 to EST_2')
        self.protocol.factory.state = state.EST_2

    def est2State():
        log.msg('Moving from EST_2 to IDLE')
        self.protocol.factory.state = state.IDLE

    def receiveState():
        log.msg('Moving from RECEIVE to IDLE')
        self.protocol.factory.state = state.IDLE
