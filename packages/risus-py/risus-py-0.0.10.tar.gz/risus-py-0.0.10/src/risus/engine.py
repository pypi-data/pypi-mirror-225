"""The risus game engine.

This module implements the "unholy trinity" of the Risus game engine:
`combat`, `single_action_conflict`, and `target_number` checks. There
is also a seperate function for `team_combat`.

These functions all support breathrough rolls as described on page 54
of the Risus companion, as well as old-fashined exploding d6s.

"""
from __future__ import annotations
from functools import cache
from typing import Callable

from icepool import Die, d, reduce, Reroll
from risus import damage_policy


def combat(
        attack_potency: int,
        enemy_potency: int,
        helper_potency: int = 0,
        damage_policy: Callable[[int, int], tuple[int, int]] = damage_policy.damage_team_mates_only,
        n_faces: int = 6,
        percent: bool = False,
        inappropriate: bool = False,
        breakthrough: bool = False,
        explode: bool = False
) -> float:
    """Simulate team combat.

    This procedure simply counts leader death as loss without attempting to
    reform the team and does not implement the double-damage self-sacrifice.

    # Arguments:
    * `attack_potency`: The potency of the team leader's cliché.
    * `helper_potency`: The total potency of the helpers' clichés.
    * `enemy_potency`: The potency of the enemy's cliché.
    * `damage_policy`: A function that takes the leader's and helpers' potencies
      and applies damage to them, returning a new pair of potencies.
    * `n_faces`: The number of faces on the dice.
    * `percent`: Whether or not to return the probability as a percent.
    * `inappropriate`: Whether or not all the team's clichés are inappropriate.
    * `breakthrough`: Whether or not to follow breakthrough rules from the Risus companion.
    * `explode`: Whether or not to roll with exploding dice.

    # Returns:
    The probability (potentially as a percentage) that the team is victorious.

    # Examples:
    >>> from risus.damage_policy import damage_team_mates_only
    >>> round(combat(5,4, percent=True), 1)
    87.8

    """
    outcome = _combat(attack_potency=attack_potency, helper_potency=helper_potency,
                      enemy_potency=enemy_potency, damage_policy=damage_policy,
                      inappropriate=inappropriate, n_faces=n_faces,
                      breakthrough=breakthrough, explode=explode)

    return outcome.probabilities(percent=percent)[1]


def single_action_conflict(
        attack_potency: int,
        enemy_potency: int,
        n_faces: int = 6,
        percent: bool = False,
        breakthrough: bool = False,
        explode: bool = False,
        **kwargs
) -> float:
    """Compute the chances of victory in a single-action conflict.

    The winner of a single action conflict is simply the higher roller. See
    Risus page 3.

    # Arguments:
    * `attack_potency`: The potency of the cliché whose chance of victory to compute.
    * `enemy_potency`: The potency of the cliché they're up against.
    * `percent`: Whether or not to return the value as a percent.
    * `n_faces`: The number of faces on the dice.
    * `breakthrough`: Whether to use breakthrough rules from the Risus Companion, page 54.
    * `explode`: Whether the attacker has exploding dice.

    # Returns:
    The probability (potentially as a percent) that the attacker is victorious.

    # Examples:
    >>> round(single_action_conflict(4, 3, percent=True), 1)
    79.5

    >>> single_action_conflict(1,6)
    0.0
    """
    attack_die = d(n_faces).explode() if explode else d(n_faces)
    attack_pool = (
        breakthrough_pool(attack_potency, attack_die) if breakthrough else attack_potency @ attack_die
    )

    enemy_die = d(n_faces)
    enemy_pool = enemy_potency @ enemy_die

    res_die = reduce(lambda a,b: Reroll if a == b else a > b, [attack_pool, enemy_pool]).simplify()
    # Catch a weird corner case where there's an automatic victory and so the
    # return is ill-formed:
    if attack_potency >= n_faces * enemy_potency:
        res_die = Die({True: 1, False: 0})

    if enemy_potency >= n_faces * attack_potency:
        res_die = Die({True: 0, False: 1})

    return res_die.probabilities(percent=percent)[1]


def target_number(
        attack_potency: int,
        enemy_potency: int,
        n_faces: int = 6,
        percent: bool = False,
        explode: bool = False,
        breakthrough: bool = False,
        **kwargs
) -> float:
    """Compute the probability that a cliché with this potency will beat the target difficulty.

    To beat the target number the roll must be equal or greater than
    the difficulty: the rules are explained on Risus page 1.

    # Arguments:
    * `attack_potency`: The potency of the cliché being rolled against.
    * `enemy_potency`: The target number to beat.
    * `percent`: Whether to return the value as a percentge rather
      than a number between 0 and 1.
    * `n_faces`: The number of faces for the dice.
    * `explode`: Whether to roll exploding dice.
    * `breakthrough`: Whether to use breakthroughs.

    # Returns:
    The probability that a cliché of this potency beats the target number.

    # Examples:
    >>> target_number(3, 10)
    0.625

    >>> target_number(4, 17, n_faces=4)
    0.0

    """
    die = d(n_faces).explode() if explode else d(n_faces)
    pool = breakthrough_pool(attack_potency, die) if breakthrough else attack_potency @ die

    res_die = pool >= enemy_potency

    # Catch a weird corner case where there's an automatic victory and so the
    # return is ill-formed:
    if attack_potency >= enemy_potency:
        # Auto-success.
        res_die = Die({True: 1, False: 0})

    if enemy_potency > n_faces * attack_potency:
        # Auto-failure
        res_die = Die({True: 0, False: 1})

    return res_die.probabilities(percent=percent)[1]


@cache
def _combat(
        attack_potency: int,
        helper_potency: int,
        enemy_potency: int,
        damage_policy: Callable[[int, int], tuple[int, int]],
        inappropriate: bool = False,
        breakthrough: bool = False,
        volunteered: bool = False,
        explode: bool = False,
        n_faces: int = 6
) -> Die:
    """Team combat internal helper.

    # Arguments:
    * `volunteered`: Whether or not the leader's potency was doubled
      by a volunteer. This flag is used to track whether or not the
      leader's dice pool was doubled last round.

    # Returns:
    A Die representing victory or defeat.

    """
    assert(not (breakthrough and explode))
    help_die = Die([0 for _ in range(n_faces-1)] + [n_faces])  # Used by non-leaders when teaming up.

    # Maybe use exploding dice:
    die = d(n_faces).explode() if explode else d(n_faces)

    # Inappropriate Cliché: see Risus page 2.
    damage = 3 if inappropriate else 1

    # Voluntarily suffer the loss: see Risus page 3.
    volunteer_potency = 2*attack_potency if volunteered else attack_potency

    # Boxcars and breakthroughs: see Risus Companion page 54.
    leader_pool = breakthrough_pool(volunteer_potency, die) if breakthrough else volunteer_potency@die
    helper_pool = helper_potency @ help_die
    team_pool = leader_pool + helper_pool
    enemy_pool = enemy_potency @ d(n_faces)

    # Base cases:
    if attack_potency > 0 and enemy_potency <= 0:
        # Team victory!
        return Die({True: 1, False: 0})

    if attack_potency <= 0 and enemy_potency > 0:
        # Enemy victory!
        return Die({True: 0, False: 1})

    # Compute outcome and results of combat.
    outcome = reduce(lambda a,b: Reroll if a == b else a > b, [team_pool, enemy_pool])

    damaged_leader, damaged_helper = damage_policy(attack_potency, helper_potency)

    if damaged_leader == attack_potency - 2 or damaged_helper == helper_potency - 2:
        volunteered = True
    else:
        volunteered = False

    team_victory = _combat(attack_potency=attack_potency,
                           helper_potency=helper_potency,
                           enemy_potency=enemy_potency-damage,
                           damage_policy=damage_policy,
                           inappropriate=inappropriate,
                           breakthrough=breakthrough,
                           volunteered=volunteered,
                           explode=explode)

    enemy_victory = _combat(attack_potency=damaged_leader,
                            helper_potency=damaged_helper,
                            enemy_potency=enemy_potency,
                            damage_policy=damage_policy,
                            inappropriate=inappropriate,
                            breakthrough=breakthrough,
                            volunteered=volunteered,
                            explode=explode)

    return outcome.if_else(team_victory, enemy_victory).simplify()


@cache
def breakthrough_pool(potency: int, die: Die, depth: int = 10) -> Die:
    """Make a dice pool that breaks through."""
    pool = potency @ die
    return pool.explode(lambda val: val == pool.max_outcome(), depth=depth)
