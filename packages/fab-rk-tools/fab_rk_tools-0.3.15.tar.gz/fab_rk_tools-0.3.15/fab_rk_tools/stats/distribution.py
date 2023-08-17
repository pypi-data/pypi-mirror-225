# Functions for calculating distribution related quantities and stats

# Owner: Gavin Bell, Optimeering AS
# Date created: 1 February 2022


import numbers

import numpy as np
import pandas as pd

TOL = 1e-4
MIN_VALUTA = 0.01  # smallest unit of currency
ROUND_DP = 2  # dp

# -------
# CUMULATIVE DISTRIBUTION
# -------


def cdf_result_from_quantiles(quantiles, values, test, inverse=False, dp=2):
    """
    Calculate either:
     - value | P(X<=value) = probabiity
     - probability => P(X<=value)

    from the CDF described by the <quantiles, values> pairs

    Inputs:
    -------
    quantiles -> list of quantiles
    values -> list of values matching the quantiles
    test -> random variable value or probability
    inverse -> boolean, inverse or plain cdf. Inverse=True => value is returned, inverse=False => probability is returned
    dp -> int, dp for result

    Outputs:
    --------
    value (inverse=False) or probability (inverse=True)

    """

    # test the quantiles and values
    if len(quantiles) != len(values):
        msg = "Quantiles and value lengths must match. Quanitles={} Values = {}".format(
            quantiles, values
        )
        raise ValueError(msg)

    # sort the quantles and values
    quantiles.sort()
    values.sort()

    if inverse:
        if test < 0 or test > 1:
            msg = f"Parameter test should be a probability (between 0 and 1). Value supplied = {test} "
            raise ValueError(msg)
        bracket_vals = quantiles
        prob_vals = values
    else:
        bracket_vals = values
        prob_vals = quantiles

    # get the row indexes bracketing the sample value
    idx = _get_bracketing_indexes(bracket_vals, test)

    # interpolate
    pos = _get_sample_pos(bracket_vals, test, idx)
    result = pos * prob_vals[idx[1]] + (1 - pos) * prob_vals[idx[0]]

    return round(result, dp)


def _get_bracketing_indexes(values, sample_value):
    """
    Get the row indexes bracketing the sample value

    If the sample value is less than the min value, returns row 0 only
    If the sample value is greater than the max value, returns the last row only
    o.w. returns the indexs of the values immediatley below and above the sample value
    """

    res = list(filter(lambda i: i > sample_value, values))
    if res == []:
        row1 = len(values) - 1
        row2 = row1
    elif res == values:
        row1 = 0
        row2 = 0
    else:
        row2 = values.index(res[0])
        row1 = row2 - 1
    return row1, row2


def _get_sample_pos(values, sample_value, idx):
    """
    Get the position of the sample value relative to the bracketing values

    pos = (s-v1)/(v2-v1)

    """
    if values[idx[0]] == values[idx[1]]:
        pos = 1
    else:
        pos = (sample_value - values[idx[0]]) / (values[idx[1]] - values[idx[0]])
    return pos
