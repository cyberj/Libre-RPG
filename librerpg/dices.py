#!/usr/bin/python
import random

class Dice():
    """Represent simple dice
    """
    name = ""
    faces = []
    critrange = []
    result = None

    def __init__(self, faces=None, nbfaces=None, critrange=None, name=None):
        """
        """
        self.faces = faces or self.faces
        self.critrange = critrange or self.critrange
        self.name = name or self.name

        if not faces:
            if isinstance(nbfaces, int):
                self.faces = range(1, nbfaces + 1 )

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

    def __str__(self):
        text = self.name
        if self.result:
            text += " : %s" % self.result
        return text

    def __int__(self):
        if not self.result:
            result = self.roll()
        else:
            result = self.result
        if not isinstance(result, int):
            raise TypeError("Result is not an Integer")
        return result

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

