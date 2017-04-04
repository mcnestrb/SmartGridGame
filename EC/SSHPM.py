import numpy as np
from twisted.python import log

class SSHPM():
    def __init__(self, en, En, price):
        self.caution = 0.5
        self.gamma = 1
        self.sigma = 0
        self.price = price
        self.en = en
        self.min = 0
        self.En = En

    def final_en(self):
        return self.en

    def solve(self):
        residual = self.getResidual()
        log.msg('Residual: {}'.format(residual))
        if (residual == 0):
            self.en = residual
            slack_var = self.En - 2 * self.caution * self.en + self.price
            log.msg('Slack Variable 1: {}\n'.format(slack_var))
            return slack_var
        else:
            z = self.getHyperplanePoint(residual)
            log.msg('Z: {}'.format(z))
            self.en = self.getEstFromHalfSpace(z)
            slack_var = self.En - self.en + self.price
            log.msg('Slack Variable 2: {}'.format(slack_var))
            log.msg('En {}'.format(self.En))
            log.msg('Current en {}\n'.format(self.en))
            return slack_var

    def getHyperplanePoint(self, residual):
        k = self.getK(0, residual)
        log.msg('K is {}'.format(k))
        eta = self.gamma ** k
        return self.en - eta * residual

    def getK(self, k, residual):
        log.msg('Left of left: {}'.format(self.functionF(self.en - (self.gamma ** k) * residual, self.En, self.price)))
        left = np.inner(self.functionF(self.en - (self.gamma ** k) * residual, self.En, self.price), residual)
        log.msg('Left: {}'.format(left))
        right = self.sigma * abs(residual) ** 2
        log.msg('Right: {}'.format(right))
        if (left >= right):
            return k
        return self.getK(k+1, residual)

    def getHalfSpace(self, z):
        z_utility = self.functionF(z, self.En, self.price)
        log.msg('Z Utility: {}'.format(z_utility))
        if (z_utility > 0):
            return {'max': z, 'min': self.min}
        elif (z_utility < 0):
            return {'max': self.En, 'min': z}
        return {'min': self.min, 'max': self.En}

    def getEstFromHalfSpace(self, z):
        half_space = self.getHalfSpace(z)
        minimum = half_space['min']
        maximum = half_space['max']
        return self.getP(self.en, minimum, maximum)

    def getResidual(self):
        log.msg('Utilty: {}'.format(self.functionF(self.en, self.En, self.price)))
        temp = self.en - self.functionF(self.en, self.En, self.price)
        log.msg('Temp: {}'.format(temp))
        y = self.getP(temp, self.min, self.En)
        log.msg('Y: {}'.format(y))
        return self.en - y

    def getP(self, x, minimum, maximum):
        y = x
        if (x < minimum):
            y = minimum
        elif (x > maximum):
            y = maximum
        return y

    def functionF(self, en, En, pn):
        # negative partial derivative of utility function with respect to en
        # U = en * pn + (En - cn * en) * en
        # dU/d en = pn - (2 * cn * en) + En
        # - dU/d en = - (pn - (2 * cn * en) + En)
        return (pn - (2 * self.caution * en) + En)

    def utility(self, en, En, price):
        return price * en + (En - self.caution * en) * en
