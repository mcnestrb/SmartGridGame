from numpy import np

class SSHPM():
    def __init__(self, en, En, price):
        self.caution = 0.5
        self.gamma = 0.5
        self.sigma = 0.5
        self.price = price
        self.en = en
        self.En = En

    def solve(self):
        remainder = getRemainder()
        if (remainder == 0):

        else:
            z = getHyperplane(remainder)

    def getHyperplane(self, remainder):
        k = getK(1, remainder)
        log.msg('{}'.format(k))
        eta = self.gamma ** k
        return self.en - eta * remainder

    def getK(self, k, remainder):
        left = np.inner(self.en - (self.gamma ** k) * remainder, remainder)
        right = self.sigma * remainder ** 2
        if (left >= right):
            return right
        return getK(k+1, remainder)

    def getHalfSpace(self):


    def getRemainder(self):
        temp = self.en - utility(self.en, self.En, self.price)
        y = temp
        if (temp < 0):
            y = 0
        elif (temp > self.En):
            y = self.En
        return self.en - y

    def utility(self, en, En, pn):
        return price * en + (En - self.caution * en) * en
