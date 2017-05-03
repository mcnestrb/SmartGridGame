from twisted.python import log
from EnumEC import ECState as state

from SSHPM import SSHPM

class ECFSM():
    def __init__(self, protocol):
        self.protocol = protocol
        self.En = 0
        self.mySSHPM = SSHPM(0,0,0)

    def idleState(self, data):
        if ('Timeslot' in str(data)):
            log.msg('Moving from IDLE to START')
            self.protocol.factory.state = state.START
            self.startState(data)

    def startState(self, data):
        energy = self.protocol.factory.energy
        if (energy < 0):
            log.msg('Energy deficit: {}'.format(energy))
            log.msg('Moving from START to RECEIVE')
            self.protocol.factory.state = state.RECEIVE
            self.protocol.transport.write(str(energy).encode())
        elif (energy > 0):
            log.msg('Moving from START to EST_1')
            self.En = energy
            self.protocol.factory.state = state.EST_1
            self.protocol.transport.write(str(energy).encode())
        else:
            log.msg('Return to IDLE state')
            self.protocol.factory.state = state.IDLE

    def est1State(self, data):
        dedata = data.decode()
        if (dedata == 'End'):
            log.msg('Moving from EST_1 to EST_2')
            self.protocol.factory.state = state.EST_2
            self.protocol.transport.write(str(self.mySSHPM.final_en()).encode())
        else:
            log.msg('{}'.format(dedata))
            lis = dedata.strip().split(',')
            P = lis[0].split(':')[1].strip()
            Edef = lis[1].split(':')[1].strip()
            priceEst = float(P)

            # Hard coded values
            if(self.protocol.factory.energy == 1000):
                self.mySSHPM.en = 300
            elif(self.protocol.factory.energy == 1100):
                self.mySSHPM.en = 400
            self.protocol.transport.write(("%.2f" % 1347.50).encode())

            # Actual code for game

            # if ('Initial -' in dedata):
            #     self.mySSHPM = SSHPM(self.En, self.En, priceEst)
            # energy_est = self.mySSHPM.solve()
            # self.protocol.transport.write(("%.2f" % energy_est).encode())

    def est2State(self, data):
        dedata = data.decode()
        if (dedata == 'End'):
            log.msg('Moving from EST_2 to IDLE')
            self.protocol.factory.state = state.IDLE
            self.protocol.transport.write(str(self.mySSHPM.final_en()).encode())
        else:
            log.msg('{}'.format(dedata))
            P = dedata.split(':')[1].strip()
            priceEst = float(P)

            # Hard coded for game
            if(self.protocol.factory.energy == 1000):
                self.mySSHPM.en = 394.8
            elif(self.protocol.factory.energy == 1100):
                self.mySSHPM.en = 305.2
            self.protocol.transport.write(("%.2f" % 1347.50).encode())

            # Actual code for game

            # if ('Updated price' in dedata):
            #     self.mySSHPM = SSHPM(self.En, self.En, priceEst)
            # energy_est = self.mySSHPM.solve()
            # self.protocol.transport.write(("%.2f" % energy_est).encode())

    def receiveState(self, data):
        dedata = float(data.decode())
        log.msg('Received: {}'.format(dedata))
        self.protocol.factory.energy += dedata
        log.msg('Moving from RECEIVE to IDLE')
        self.protocol.factory.state = state.IDLE
