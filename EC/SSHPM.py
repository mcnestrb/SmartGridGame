import numpy as np
from twisted.python import log

class SSHPM():
    def __init__(self, en, En, price):
        self.caution = 0.5
        self.gamma = 0.5
        self.sigma = 0.5
        self.price = price
        self.en = en
        self.min = 0
        self.En = En

    def final_en(self):
        return self.en

    def solve(self):
        remainder = self.getRemainder()
        log.msg('Remainder: {}'.format(remainder))
        if (remainder == 0):
            z = self.getHyperplanePoint(remainder)
            log.msg('Z: {}'.format(z))
            next_en = self.getEstFromHalfSpace(z)
            log.msg('Next en: {}'.format(next_en))
            self.en = next_en
            thing = self.En - 2 * self.caution * self.en + self.price
            log.msg('Thing: {}'.format(thing))
            log.msg('En {}'.format(self.En))
            log.msg('price {}\n'.format(self.price))
            return self.En - 2 * self.caution * self.en + self.price
        else:
            z = self.getHyperplanePoint(remainder)
            log.msg('Z: {}'.format(z))
            next_en = self.getEstFromHalfSpace(z)
            log.msg('Next en: {}'.format(next_en))
            curr_en = self.en
            self.en = next_en
            thing2 = self.En - curr_en + self.price
            log.msg('Thing2: {}'.format(thing2))
            log.msg('En {}'.format(self.En))
            log.msg('Current en {}'.format(curr_en))
            log.msg('price {}\n'.format(self.price))
            return self.En - curr_en + self.price

    def getHyperplanePoint(self, remainder):
        k = self.getK(1, remainder)
        log.msg('K is {}'.format(k))
        eta = self.gamma ** k
        return self.en - eta * remainder

    def getK(self, k, remainder):
        left = np.inner(self.en - (self.gamma ** k) * remainder, remainder)
        right = self.sigma * remainder ** 2
        if (left >= right):
            return k
        return getK(k+1, remainder)

    def getHalfSpace(self, z):
        z_utility = self.utility(z, self.En, self.price)
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
        return self.getPC(self.en, minimum, maximum)

    def getRemainder(self):
        temp = self.en - self.utility(self.en, self.En, self.price)
        log.msg('Temp: {}'.format(temp))
        y = self.getPC(temp, self.min, self.En)
        log.msg('Y: {}'.format(y))
        return self.en - y

    def getPC(self, x, minimum, maximum):
        y = x
        if (x < minimum):
            y = minimum
        elif (x > maximum):
            y = maximum
        return y

    def utility(self, en, En, price):
        log.msg('Utility: {}'.format(price * en + (En - self.caution * en) * en))
        return price * en + (En - self.caution * en) * en
