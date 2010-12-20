class Throw():
    """A throw to manage multiple dices"""
    results = []
    raw_results = []
    mod = 0
    rules = []

    @property
    def total(self):
        """Get total"""
        return sum(self.results) + self.mod

    def __init__(self, results):
        """Initialize throw"""
        self.raw_results = list(results)
        self.results = results

    def __int__(self):
        return self.total

class BaseSystem():
    """base DiceSystem"""
    dices = []
    results = []
    rules = []
    mod = 0

    def roll_dices(self, mod=0):
        """Roll all dices
        """
        self.mod = mod or self.mod

        results = []
        for dice in self.dices:
            results.append(dice.clone())

        throw = Throw(results)

        return throw

    def throw(self, mod=0):
        """Roll dices and apply rules
        return throw
        """
        throw = self.roll_dices(mod)

        for rule in self.rules:
            rule(self, throw)
            throw.rules.append(rule)

        return throw

    def simple_throw(self, mod=0):
        """Roll dices and apply rules
        return int
        """
        throw = self.throw(mod)
        return int(throw)
