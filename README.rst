=========
Libre RPG
=========

Yet another open RPG engine...

Features
========

 * Dice roll
 * Custimizable Throw systems and rules
 * Tests : 100% code coverage

Examples
========

Simple dices::

    from librerpg.dices import D20, D6
    if D20() >= 15:
        print "Ok, success."

    # Throw 3 D6 and add 3
    result = 3*D6() + 3
    
    #Custom
    from librerpg.dices import Dice
    result = 3*Dice(faces=[2,3,4,5]) + 3

``Throw`` system::

    from librerpg.dices import Throw, D100
    result = Throw.direct("2D6+5")
    # ex : result = 15
    result = Throw.direct(D100())

    # Show dices
    throw = Throw("2D8")
    print throw.results
    # ex : throw.results = [1, 7]
    # Reroll all
    new_total = throw.reroll()

    # Use custom fumble'o'matic dice
    # The rules sets variables on Throw like throw.fumble if rules matches 
    from librerpg.dices import Dice, rules
    class MyThrow(Throw):
        dices = [Dice(faces=[1])]
        rules = [
           rules.FumbleRule(),
           rules.OpenEndedDieRule(oed_limit=95)
        ]

    throw = MyThrow()
    if throw.fumble:
        print "Sorry dave..."

    # Now use critic'o'matic dices
    throw.dices = [Dice(faces=[98, 99])]
    throw.reroll()


Tests
=====

Just launch::

    make test
