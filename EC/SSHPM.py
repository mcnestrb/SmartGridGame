from numpy import np

class SSHPM():
    def __init__(self, en, En, price):
        self.caution = 0.5
        self.gamma = 0.5
        self.sigma = 0.5
        self.price = price
        self.en = en
        self.min = 0
        self.max = En
        self.En = En

    def solve(self):
        remainder = getRemainder()
        if (remainder == 0):
            z = getHyperplanePoint(remainder)
            next_en = getEstFromHalfSpace(z)
            self.en = next_en
            return {'EMES': self.En - 2 * self.caution * self.en + self.price}
        else:
            z = getHyperplanePoint(remainder)
            next_en = getEstFromHalfSpace(z)
            curr_en = self.en
            self.en = next_en
            return {'NO EMES': self.En - curr_en + self.price}

    def getHyperplanePoint(self, remainder):
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

    def getEstFromHalfSpace(self, z):
        if (z > self.en):
            self.min = z
        elif (z < self.en):
            self.max = z
        return (self.max + self.min) / 2

    def getRemainder(self):
        temp = self.en - utility(self.en, self.max, self.price)
        y = getPC(temp)
        return self.en - y

    def getPC(self, x):
        y = x
        if (x < self.min):
            y = self.min
        elif (x > self.max):
            y = self.max
        return y

    def utility(self, en, En, price):
        return price * en + (En - self.caution * en) * en
