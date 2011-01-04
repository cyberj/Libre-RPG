import unittest
import sys
import os

sys.path[0:0] = [os.path.join(os.path.dirname(__file__), ".."),]

from librerpg.dices import Dice, D2, D4, D6, D8, D10, D12, D20, D100, Coin
from librerpg.dices import rules, Throw

class TestDice(unittest.TestCase):
    """Test librerpg.dices.Dice class
    """
    def setUp(self):
        pass

    def test_dice(self):
        """Basic tests for Dice
        """
        dice = Dice()
        self.assertRaises(Exception, dice.roll)
        dice.faces = [1, 1, 1, 1]
        result = dice.roll()
        self.assertEqual(result, 1)
        dice.faces = [2, 2, 2, 2]
        result = dice.roll()
        self.assertEqual(result, 2)

        # With params
        dice = Dice(nbfaces=4)
        self.assertEquals(dice.faces, [1, 2, 3, 4])
        result = dice.roll()
        self.assertTrue(result in [1, 2, 3, 4])

        # Various dices
        dice = D2()
        self.assertTrue(str(dice).startswith("D2"))
        dice = D100()
        result = dice.roll()
        result2 = int(dice)
        self.assertEquals(result, result2)
        self.assertEquals(str(dice), "D100 : %s" % result)
        dice = D20()
        result = int(dice)
        coin = Coin()
        self.assertRaises(TypeError, int, coin)
        self.assertTrue(coin.result in ["Heads", "Tails"])
        result = coin.flip()
        result = D6.throw()

        # Test clone
        adice = Dice(faces=range(100000))
        anotherdice = adice.clone()
        self.assertNotEquals(adice.result, anotherdice.result)

        # Test repr
        dices = [D6(), D6()]
        strdices = str(dices)
        expct = "[<D6 : %s>, <D6 : %s>]" % tuple(x.result for x in dices)
        self.assertEquals(strdices, expct)
        dices = [Dice(faces=[1]), Dice(faces=[1])]
        strdices = str(dices)
        expct = "[<Dice : %s>, <Dice : %s>]" % tuple(x.result for x in dices)
        self.assertEquals(strdices, expct)

    def test_math(self):
        """Try some math
        """
        results = []
        for x in range(1000):
            result = 3 * D6() + 5
            self.assertTrue(result <= 23)
            self.assertTrue(result >= 8)
            if result not in results:
                results.append(result)
        self.assertTrue(len(results) > 6)

        result = 3 * D6() + 5 + D100()
        result = D6() * D4() + 5 + D100() + D12()
        result = D6() * D4() + 5 + D100() + 2 * D12()

        # Compare
        self.assertTrue(D6() < Dice(faces=[15,16,17]))
        self.assertFalse(D6() > Dice(faces=[15,16,17]))
        self.assertTrue(1 < Dice(faces=[15,16,17]))
        self.assertTrue(20 > Dice(faces=[15,16,17]))
        self.assertFalse(1 > Dice(faces=[15,16,17]))
        self.assertFalse(20 < Dice(faces=[15,16,17]))

class TestThrows(unittest.TestCase):
    """Test librerpg.dices.Throws
    """
    class OEDThrow(Throw):
        rules = [rules.OpenEndedDieRule(oed_limit=95)]
        dices = [D100(faces=[97])]

    def test_rules(self):
        """Basic tests for Dice System
        """
        throw = Throw(D6())
        # Normal test
        result = throw.total
        self.assertTrue(isinstance(result, int))

        # Some math
        self.assertNotEquals(result, 0)
        self.assertTrue(result > 0)
        self.assertTrue(result <= 6)

        # Check random, dice must be independants
        throw = Throw([D6() for x in range(20)])
        dice_set = set([int(x) for x in throw.results])
        self.assertTrue(len(dice_set) > 1)

        # Check with rules
        throw.rules = [rules.FumbleRule()]
        throw.dices = [Dice(faces=[1])]
        throw.reroll()
        self.assertTrue(throw.fumble)
        throw.dices = [Dice(faces=[3])]
        throw.reroll()
        self.assertFalse(throw.fumble)
        throw.rules = [rules.FumbleRule(fumble_range=[3])]
        throw.apply_rules()
        self.assertTrue(throw.fumble)
        # Direct test
        throwtotal = self.OEDThrow.direct()
        self.assertEquals(throwtotal, 4*97)
        throw = self.OEDThrow()
        self.assertEquals(throw.total, 4*97)
        throw.rules[0].auto_oed = False
        total = throw.reroll()
        self.assertEquals(throw.total, 97)
        # Empty
        throw.rules.append(rules.Rule())
        self.assertRaises(NotImplementedError, throw.reroll)

        # Critic test
        throw = Throw(Dice(faces=[20]))
        throw.rules = [rules.CriticRule([20])]
        throw.reroll()
        self.assertEqual(throw.total, 40)

    def test_basethrow(self):
        """Test dice throws
        """
        # Dices throw
        throw = Throw(D20(), mod=5)
        self.assertEqual(throw.mod, 5)
        self.assertEqual(throw.rawtotal + 5, throw.total)
        result = throw.total
        self.assertTrue(result <= 25)
        self.assertTrue(result >= 5)
        # Dice list
        dice = D20()
        dice.result = 20
        throw = Throw([dice, dice], mod=5)
        result = throw.total
        self.assertTrue(result == 45)
        # Text throw
        throw = Throw("2D6+3")
        result = throw.total
        self.assertTrue(result <= 15)
        self.assertTrue(result >= 5)
        throw = Throw("D20-3")
        result = throw.total
        self.assertTrue(result <= 17)
        self.assertTrue(result > -3)
        throw = Throw("D3")
        result = int(throw)
        self.assertTrue(result <= 3)
        self.assertTrue(result > 0)
        self.assertRaises(ValueError, Throw, "Some Dice+4")


if __name__ == '__main__':
    unittest.main()

