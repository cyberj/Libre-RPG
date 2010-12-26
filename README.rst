=========
Libre RPG
=========

Yet another open RPG engine...

Features
========

 * 100% code coverage
 * Dice roll
 * Customizables Rpg dice systems

Examples
========

Simple dices throws::

    from librerpg.dices import D20, D6
    if D20() >= 15:
        print "Ok, success."

    # Throw 3 D6 and add 3
    result = 3*D6() + 3

See ``librerpg.dices.systems.AbfSystem`` for custom class::

    from librerpg.dices.systems import BaseSystem
    system = AbfSystem()
    result = system.simple_throw()

    # Use fumble'o'matic dice
    from librerpg.dices import Dice
    fumble_dice = Dice(faces=range(1,5))
    system.dices = [fumble_dice]
    throw = system.throw()
    if throw.fumble:
        print "Sorry dave..."

Tests
=====

Just launch::

    make test
