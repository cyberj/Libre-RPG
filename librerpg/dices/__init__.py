import random
import re
from copy import copy

class Dice():
    """Represent simple dice
    """
    name = ""
    faces = []
    result = None

    def __init__(self, faces=None, nbfaces=None, name=None):
        """
        """
        self.faces = faces or self.faces
        self.name = name or self.name

        if not faces:
            if isinstance(nbfaces, int):
                self.faces = range(1, nbfaces + 1 )

        if self.faces:
            self.roll()

    @classmethod
    def throw(cls, *args, **kwargs):
        """Roll dice get direct result
        """
        dice = cls(*args, **kwargs)
        return dice.roll()

    def roll(self):
        """Roll the dice, get the result
        """
        if not self.faces:
            raise Exception("No faces on this dice")
        self.result = random.choice(self.faces)
        return self.result

    def clone(self):
        """Clone dice for multiple throws
        """
        cloned = copy(self)
        cloned.roll()
        return cloned

    def __str__(self):
        if self.name:
            text = self.name
        else:
            text = "Dice"
        if self.result:
            text += " : %s" % self.result
        return text

    def __repr__(self):
        return "<%s>" % self.__str__()

    def __int__(self):
        result = self.result
        if not isinstance(result, int):
            raise TypeError("Result is not an Integer")
        return result

    def __cmp__(self, other):
        return cmp(int(self), other)

    def __radd__(self, other):
        return int(self) + other

    def __mul__(self, other):
        return int(self) * other

    def __rmul__(self, other):
        result = 0
        for dice in range(other):
            result += self.roll()
        return result

class Throw():
    """A throw to manage multiple dices"""
    results = []
    dices = []
    mod = 0
    rules = []

    @property
    def rawtotal(self):
        """Get total withour mods"""
        # print self.results
        return sum(self.results)

    @property
    def total(self):
        """Get total"""
        return self.rawtotal + self.mod

    def apply_rules(self, reset=True):
        """Apply rules
        """
        if reset:
            self.results = list(self.dices)

        for rule in self.rules:
            rule.apply(self)

    def reroll(self):
        """Reroll all dices and apply rules if any
        """
        for x in self.dices:
            x.roll()
        self.apply_rules(reset=True)
        return self.total

    def __init__(self, dices=None, mod=None):
        """Initialize throw"""
        self.mod = mod or self.mod

        if dices:
            if isinstance(dices, Dice):
                # Simpledice
                self.dices = [dices]
            elif hasattr(dices, '__iter__'):
                self.dices = dices
            elif isinstance(dices, str) or isinstance(dices, unicode):
                dices = dices.upper()
                pattern = r"(?P<nb>[0-9])*(?P<dice>D[0-9]+)"
                pattern += r"(?P<neg>[\+\-]?)(?P<mod>[0-9]*)"
                match = re.search(pattern, dices)
                if not match:
                    raise ValueError("Wrong dice patern")
                results = match.groupdict()

                # Find dice
                if results['dice'] in DICES.keys():
                    dice = DICES[results["dice"]]()
                else:
                    faces = int(results['dice'][1:])
                    dice = Dice(faces=range(1,faces))

                # Find number
                nb = int(results['nb'] or 1)

                # Find mod
                tmod = int(results['mod'] or 0)
                neg = results['neg'] or "+"
                if neg == "-" and tmod != 0:
                    tmod = -tmod

                # result
                self.dices = [dice.clone() for x in range(nb)]
                self.mod = tmod

        self.results = list(self.dices)
        self.apply_rules()

    def __int__(self):
        return self.total

    @classmethod
    def direct(cls, *args, **kwargs):
        """Roll dice get direct result
        """
        throw = cls(*args, **kwargs)
        return throw.total


# Bunch of classic dices :
class D2(Dice):
    faces = range(1,3)
    name = "D2"

class D4(Dice):
    faces = range(1,5)
    name = "D4"

class D6(Dice):
    faces = range(1,7)
    name = "D6"

class D8(Dice):
    faces = range(1,9)
    name = "D8"

class D10(Dice):
    faces = range(1,11)
    name = "D10"

class D12(Dice):
    faces = range(1,13)
    name = "D12"

class D20(Dice):
    faces = range(1,20)
    name = "D20"

class D100(Dice):
    faces = range(1,101)
    name = "D100"

class Coin(Dice):
    faces = ["Heads", "Tails"]
    name = "Coin"
    flip = Dice.roll

DICES = {
    "D2" : D2,
    "D4" : D4,
    "D6" : D6,
    "D8" : D8,
    "D10" : D10,
    "D12" : D12,
    "D20" : D20,
    "D100" : D100,
    }

