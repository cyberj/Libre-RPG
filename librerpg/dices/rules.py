"""
Commons dices rules
"""

def fumble(system, throw):
    """Apply rule to a Throw
    """
    fumble_range = getattr(system, "fumble_range", None) or [1]
    throw.fumble = False
    for dice in throw.raw_results:
        if dice in fumble_range:
            throw.fumble = True
    return throw.fumble

