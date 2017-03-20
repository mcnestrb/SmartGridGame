from twisted.python import log
from EnumEC import ECState as state

class ECFSM():
    def __init__(self, protocol):
        self.protocol = protocol

    def idleState(self, data):
        if ('Timeslot' in str(data)):
            log.msg('Moving from IDLE to START')
            self.protocol.factory.state = state.START
            self.startState(data)

    def startState(self, data):
        string = 'What\'s your energy for %s\n' % (data.decode())
        energy = int(input(string))
        if (energy < 0):
            log.msg('Moving from START to RECEIVE')
            self.protocol.factory.state = state.RECEIVE
            self.protocol.transport.write(str(energy).encode())
        elif (energy > 0):
            log.msg('Moving from START to EST_1')
            self.protocol.factory.state = state.EST_1
            self.protocol.transport.write(str(energy).encode())
        else:
            log.msg('Return to IDLE state')
            self.protocol.factory.state = state.IDLE

    def est1State(self, data):
        log.msg('{}'.format(data.decode()))
        lis = data.decode().strip().split(',')
        p = lis[0].strip().split(':')[1]
        Edef = lis[1].strip().split(':')[1]
        N = lis[2].strip().split(':')[1]
        log.msg('P is %s and Edef is %s and N is %s' % (p, Edef, N))
        log.msg('Moving from EST_1 to EST_2')
        self.protocol.factory.state = state.EST_2

    def est2State(self, data):
        log.msg('Moving from EST_2 to IDLE')
        self.protocol.factory.state = state.IDLE

    def receiveState(self):
        log.msg('Moving from RECEIVE to IDLE')
        self.protocol.factory.state = state.IDLE
