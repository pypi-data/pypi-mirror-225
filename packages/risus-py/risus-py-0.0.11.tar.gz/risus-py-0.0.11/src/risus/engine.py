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
from risus.dice import make_pool, compare_with_reroll

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
        percent: bool = False,
        n_faces: int = 6,
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

    Also takes keyword arguments as for `risus.dice.make_pool`. These
    affect only the attacker.

    # Returns:
    The probability (potentially as a percent) that the attacker is
    victorious.

    # Examples:
    >>> round(single_action_conflict(4, 3, percent=True), 1)
    79.5

    >>> single_action_conflict(1,6)
    0.0

    """
    attack_pool = make_pool(attack_potency, helper=False, n_faces=n_faces, **kwargs)
    enemy_pool = make_pool(enemy_potency, helper=False, n_faces=n_faces)

    res_die = compare_with_reroll(attack_pool, enemy_pool)

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
    pool = make_pool(attack_potency, n_faces=n_faces, helper=False, **kwargs)
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
        volunteered: bool = False,
        n_faces: int = 6,
        **kwargs
) -> Die:
    """Team combat internal helper.

    # Arguments:
    * `volunteered`: Whether or not the leader's potency was doubled
      by a volunteer. This flag is used to track whether or not the
      leader's dice pool was doubled last round.

    # Returns:
    A Die representing victory or defeat.

    """
    # Inappropriate Cliché: see Risus page 2.
    damage = 3 if inappropriate else 1

    # Voluntarily suffer the loss: see Risus page 3.
    volunteer_potency = 2*attack_potency if volunteered else attack_potency

    # Prepare the team's pool. For now, only the leader's dice are assumed to explode.
    leader_pool = make_pool(volunteer_potency, n_faces=n_faces, helper=False, **kwargs)
    helper_pool = make_pool(helper_potency, n_faces=n_faces, helper=True)
    team_pool = leader_pool + helper_pool

    enemy_pool = make_pool(enemy_potency, n_faces=n_faces)

    # Base cases:
    if attack_potency > 0 and enemy_potency <= 0:
        # Team victory!
        return Die({True: 1, False: 0})
    if attack_potency <= 0 and enemy_potency > 0:
        # Enemy victory!
        return Die({True: 0, False: 1})

    # Compute outcome and results of combat.
    outcome = compare_with_reroll(team_pool, enemy_pool)
    damaged_leader, damaged_helper = damage_policy(attack_potency, helper_potency)

    # Check whether someone volunteered to take damage: see Risus page 3.
    if damaged_leader == attack_potency - 2 or damaged_helper == helper_potency - 2:
        volunteered = True
    else:
        volunteered = False

    # Recursive calls to self.
    team_victory = _combat(attack_potency=attack_potency,
                           helper_potency=helper_potency,
                           enemy_potency=enemy_potency-damage,
                           damage_policy=damage_policy,
                           inappropriate=inappropriate,
                           volunteered=volunteered,
                           **kwargs)

    enemy_victory = _combat(attack_potency=damaged_leader,
                            helper_potency=damaged_helper,
                            enemy_potency=enemy_potency,
                            damage_policy=damage_policy,
                            inappropriate=inappropriate,
                            volunteered=volunteered,
                            **kwargs)

    # And mix together the outcomes!
    return outcome.if_else(team_victory, enemy_victory).simplify()
