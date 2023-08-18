"""Policies for distributing damage in team combat.

These all expect two integers, the leader and the team potencies, and
returns a pair of integers, the new potencies with damage
applied. These are not expected to take the post-vonlunteer doubling
and halving into account: this is handled by `engine.team_combat`. See
Risus page 3 for more details.

"""

def damage_team_mates_only(leader_potency: int, helper_potency: int) -> tuple[int, int]:
    """Deduct one from the helpers, unless there are no more helpers.

    Examples:
    ---------
    >>> damage_team_mates_only(4, 3)
    (4, 2)

    >>> damage_team_mates_only(5, 0)
    (4, 0)
    """
    return (leader_potency, helper_potency-1) if helper_potency else (leader_potency-1,helper_potency)


def damage_volunteer(leader_potency: int, helper_potency: int) -> tuple[int, int]:
    """Deal double damage to a helper if they can take it, then the
    leader if they can take it, then fall back on dealing one damage
    to whoever can absorb it.

    Examples:
    ---------
    >>> damage_volunteer(4, 5)
    (4, 3)

    >>> damage_volunteer(4, 1)
    (2, 1)

    >>> damage_volunteer(2, 1)
    (2, 0)
    """
    if helper_potency >= 2:
        return (leader_potency, helper_potency-2)

    elif leader_potency > 2:
        return (leader_potency-2, helper_potency)

    elif helper_potency > 0:
        return (leader_potency, helper_potency-1)

    else:
        return (leader_potency-1, helper_potency)
