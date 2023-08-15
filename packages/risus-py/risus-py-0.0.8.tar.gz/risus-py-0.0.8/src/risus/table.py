"""Make tables."""

from __future__ import annotations
from typing import Callable

import numpy as np
import pandas as pd

from risus.engine import target_number, combat, single_action_conflict, team_combat


def make_target_number_table(
        max_potency: int,
        n_faces: int = 6,
        **kwargs
) -> pd.DataFrame:

    """Make a dataframe comparing potencies to target numbers.

    This table includes all the target numbers up to the maximum possible for
    the highest potency (that is, 6*max_potency).

    # Arguments:
    * `max_potency`: The highest potency to consider.
    * `n_faces`: How many faces the dice should have.

    # Returns:
    A DataFrame whose columns are the potencies, whose rows are the target
    numbers, and whose contents are the probability (as a percentage) that a
    cliché of that potency would beat that target number.

    # Examples:
    >>> make_target_number_table(4, percent=True).round(1)
            1      2      3      4
    1   100.0  100.0  100.0  100.0
    2    83.3  100.0  100.0  100.0
    3    66.7   97.2  100.0  100.0
    4    50.0   91.7   99.5  100.0
    5    33.3   83.3   98.1   99.9
    6    16.7   72.2   95.4   99.6
    7     0.0   58.3   90.7   98.8
    8     0.0   41.7   83.8   97.3
    9     0.0   27.8   74.1   94.6
    10    0.0   16.7   62.5   90.3
    11    0.0    8.3   50.0   84.1
    12    0.0    2.8   37.5   76.1
    13    0.0    0.0   25.9   66.4
    14    0.0    0.0   16.2   55.6
    15    0.0    0.0    9.3   44.4
    16    0.0    0.0    4.6   33.6
    17    0.0    0.0    1.9   23.9
    18    0.0    0.0    0.5   15.9
    19    0.0    0.0    0.0    9.7
    20    0.0    0.0    0.0    5.4
    21    0.0    0.0    0.0    2.7
    22    0.0    0.0    0.0    1.2
    23    0.0    0.0    0.0    0.4
    24    0.0    0.0    0.0    0.1

    >>> make_target_number_table(4, n_faces=4, explode=True).round(3)
           1      2      3      4
    1   1.00  1.000  1.000  1.000
    2   0.75  1.000  1.000  1.000
    3   0.50  0.938  1.000  1.000
    4   0.25  0.812  0.984  1.000
    5   0.00  0.625  0.938  0.996
    6   0.00  0.500  0.844  0.980
    7   0.00  0.406  0.734  0.941
    8   0.00  0.344  0.629  0.879
    9   0.00  0.000  0.547  0.801
    10  0.00  0.000  0.461  0.723
    11  0.00  0.000  0.379  0.645
    12  0.00  0.000  0.303  0.566
    13  0.00  0.000  0.000  0.486
    14  0.00  0.000  0.000  0.414
    15  0.00  0.000  0.000  0.350
    16  0.00  0.000  0.000  0.295

    """
    return make_table(target_number, max_potency, n_faces*max_potency, 0, n_faces=n_faces, **kwargs).T


def make_combat_victory_table(max_potency: int, **kwargs):
    """Make a square dataframe with `engine.combat`.

    # Examples:
    >>> make_combat_victory_table(6, percent=True).round(1)
           1      2      3     4     5     6
    1   50.0    5.0    0.1   0.0   0.0   0.0
    2   95.0   50.0    8.2   0.3   0.0   0.0
    3   99.9   91.8   50.0  10.5   0.7   0.0
    4  100.0   99.7   89.5  50.0  12.2   1.1
    5  100.0  100.0   99.3  87.8  50.0  13.7
    6  100.0  100.0  100.0  98.9  86.3  50.0

    """
    return make_table(combat, max_potency, max_potency, 0, **kwargs)


def make_single_action_conflict_table(max_potency: int, **kwargs):
    """Make a square single-action conflict dataframe.

    # Examples:
    >>> make_single_action_conflict_table(8, n_faces=8, percent=True).round(1)
           1      2     3     4     5     6     7     8
    1   50.0   11.6   1.7   0.2   0.0   0.0   0.0   0.0
    2   88.4   50.0  17.9   4.6   0.9   0.1   0.0   0.0
    3   98.3   82.1  50.0  22.0   7.4   2.0   0.5   0.1
    4   99.8   95.4  78.0  50.0  24.8   9.9   3.3   0.9
    5  100.0   99.1  92.6  75.2  50.0  27.0  12.0   4.6
    6  100.0   99.9  98.0  90.1  73.0  50.0  28.6  13.9
    7  100.0  100.0  99.5  96.7  88.0  71.4  50.0  30.0
    8  100.0  100.0  99.9  99.1  95.4  86.1  70.0  50.0

    """
    return make_table(single_action_conflict, max_potency, max_potency, 0, **kwargs)


def make_team_combat_table(player_potency: int, n_helpers: int, enemy_potency: int, **kwargs):
    """Make a team combat table.
    """
    return make_table(player_potency, n_helpers*player_potency, enemy_potency, **kwargs)


def make_table(
        compare_func: Callable[..., float],
        x_axis: int,
        y_axis: int,
        z_axis: int,
        **kwargs
) -> pd.DataFrame:
    """Make a victory table of arbitrary shape for a comparison function.

    # Arguments:
    * `compare_func`: The comparison function to use.
    * `x_axis`: The shape in the first axis.
    * `y_axis`: The shape in the second axis.
    * `z_axis`: The shape in the third axis.

    Also accepts keyword arguments as for `risus.engine`.

    # Returns: 
    A DataFrame of floats, or a DataFrame of series where z_axis > 0.

    # Examples:
    >>> from risus.engine import combat
    >>> make_table(combat, 6, 10, 0, percent=True, explode=True).round(1)
          1      2      3     4     5     6     7    8    9    10
    1   51.6    9.1    0.3   0.0   0.0   0.0   0.0  0.0  0.0  0.0
    2   95.0   55.6   14.5   1.1   0.0   0.0   0.0  0.0  0.0  0.0
    3   99.9   92.5   58.0  18.2   2.1   0.1   0.0  0.0  0.0  0.0
    4  100.0   99.7   91.3  59.6  21.1   3.1   0.2  0.0  0.0  0.0
    5  100.0  100.0   99.4  90.6  60.9  23.5   4.2  0.3  0.0  0.0
    6  100.0  100.0  100.0  99.2  90.2  61.8  25.5  5.1  0.4  0.0
    """
    # Whoosh...
    return pd.DataFrame({leader_potency:
                         {enemy_potency:
                          pd.Series({helper_potency: compare_func(attack_potency=leader_potency,
                                                                  helper_potency=helper_potency,
                                                                  enemy_potency=enemy_potency,
                                                                  **kwargs)
                                     for helper_potency
                                     in range(0, z_axis+1)}).squeeze()
                          for enemy_potency
                          in range(1, y_axis+1)}
                         for leader_potency
                         in range(1, x_axis+1)}).T
