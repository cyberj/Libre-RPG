"""
Commons dices rules
"""

class Rule():
    """BaseRule
    """
    def apply(self, throw):
        """Apply rule on throw
        """
        raise NotImplementedError()

class FumbleRule(Rule):
    fumble_range = [1]

    def __init__(self, fumble_range=[1]):
        self.fumble_range = fumble_range

    def apply(self, throw):
        """Apply rule to a Throw
        """
        throw.fumble = False
        for dice in throw.results:
            if dice in self.fumble_range:
                throw.fumble = True
        return throw.fumble

class OpenEndedDieRule(Rule):
    oed_limit = None
    auto_oed = True

    def __init__(self, oed_limit):
        self.oed_limit = oed_limit

    def apply(self, throw):
        """Apply "Open Ended Die" rule
        """
        oed_limit = self.oed_limit

        throw.oed_results = []
        for dice in throw.results:
            oed = dice
            while oed >= oed_limit and self.auto_oed:
                oed = oed.clone()
                throw.oed_results.append(oed)
                oed_limit +=1
        throw.results = throw.results + throw.oed_results

        return bool(throw.oed_results)
