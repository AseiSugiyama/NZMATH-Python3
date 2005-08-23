"""
The module is for trial division factorization method.
"""

class FactoringInteger:
    """
    A class for factorization.
    The class has two attributes: number and factors.
    """
    def __init__(self, number):
        self.number = number
        self.factors = []

    def register(self, divisor):
        """
        Register a divisor of the number, if the divisor is a true
        divisor of the number.  The number is divided by the divisor
        as many times as possible.
        """
        valuation = 0
        while not (self.number % divisor):
            self.number //= divisor
            valuation += 1
        if valuation:
            self.factors.append((divisor, valuation))

def trialDivision(n):
    """
    Factor the given number by the trial division method.
    """
    target = FactoringInteger(n)
    for d in (2, 3, 5):
        if d**2 > target.number:
            break
        if not (target.number % d):
            target.register(d)
    d = 7
    j = 0
    # steps to make a sequence coprime to 30
    steps = (4, 2, 4, 2, 4, 6, 2, 6)
    while d**2 <= target.number:
        if not (target.number % d):
            target.register(d)
        d += steps[j]
        if j == 7:
            j = 0
        else:
            j += 1
    if target.number != 1:
        target.register(target.number)
    return target.factors
