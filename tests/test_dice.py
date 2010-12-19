import unittest
import sys
import os

sys.path[0:0] = [os.path.join(os.path.dirname(__file__), ".."),]

from librerpg.dices import Dice, D2, D4, D6, D8, D10, D12, D20, D100, Coin

class TestDice(unittest.TestCase):

    def setUp(self):
        self.seq = range(10)

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
        self.assertEquals(str(dice), "D2")
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

    def test_math(self):
        """Try some math
        """
        for x in range(1000):
            result = 3 * D6() + 5
            self.assertTrue(result <= 23)
            self.assertTrue(result >= 8)

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

if __name__ == '__main__':
    unittest.main()

