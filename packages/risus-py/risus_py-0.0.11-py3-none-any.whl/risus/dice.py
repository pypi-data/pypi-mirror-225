"""Create dice pools.

This module exposes two major functions: `make_pool` and `compare_with_reroll`.

They are used throughout `risus.engine` to compute the outcome of rolls.

"""

from icepool import d, Die, Reroll, reduce


def make_pool(
        potency: int,
        n_faces: int = 6,
        helper: bool = False,
        breakthrough: bool = False,
        explode: bool = False,
        **kwargs
) -> Die:
    """Make a potency-sized pool of die, potentially for helpers, exploding and breakthrough.

    # Arguments:
    * `potency`: The sice of the pool to build.
    * `n_faces`: The number of faces on the dice.
    * `helper`: Whether to build a pool of help dice.
    * `breakthrough`: Whether to use breakthrough rules from the Risus Companion, page 54.
    * `explode`: Whether the attacker has exploding dice.

    # Examples:
    >>> make_pool(3, n_faces=6)
    Die({3: 1, 4: 3, 5: 6, 6: 10, 7: 15, 8: 21, 9: 25, 10: 27, 11: 27, 12: 25, 13: 21, 14: 15, 15: 10, 16: 6, 17: 3, 18: 1})

    """
    die = help_d(n_faces) if helper else d(n_faces)
    die = die.explode() if explode else die
    pool = (potency@die).explode() if breakthrough else potency@die
    return pool.simplify()


def compare_with_reroll(pool_1: Die, pool_2: Die):
    """Compare `pool_1` with `pool_2`.

    # Return

    A Die with True results for whenever `pool_1` is greater than
    `pool_2` and False for when it is less: reroll in case of
    equality.

    # Examples
    >>> from icecup import d
    >>> (d(6) > d(6)).simplify()
    Die({False: 7, True: 5})
    >>> compare_with_reroll(d(6), d(6))
    Die({False: 1, True: 1})

    """
    return reduce(lambda a,b: Reroll if a == b else a > b, [pool_1, pool_2]).simplify()


def help_d(n_faces: int) -> Die:
    """Make a die all of whose outcomes are 0 except for the maximum."""
    return Die([0 for _ in range(n_faces-1)] + [n_faces])
