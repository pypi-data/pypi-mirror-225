"""
Fab derived data

These tools are to calculate derived data series.
They may at a later point be moved to the API??

    - rk_nordic_api -> calculate the LPI (large price index) series.
            Alternative calc methods enabled.
"""
from typing import Union

import archimedes

# import numpy as np
import pandas as pd

from ..common.constants import PermittedTimeZones

LPI_METHODS = [
    "constant_abs",
    "constant_perc",
]


def rk_nordic_lpi(
    method: str,
    direction: str,
    price_areas: Union[list, str],
    start: Union[pd.Timestamp, str],
    end: Union[pd.Timestamp, str] = None,
) -> pd.DataFrame:
    """
    Calculates and returns the LPI series for rk prices in the given price
    areas between start and end datetimes.

    Returns the series in a dataframe with a single column for the lpi per
    price area, indexed by datetime

    The LPI is binary: a value of 1 -> the price deviation is large,
    0 -> the price deviation is not large

    Parameters:
        method: str -> {"constant_abs", "constant_perc"},
        direction: str -> {"up", "dn"},
        price_areas: Union[list, str] -> list of strings, or single string,
                price area codes
        start: Union[pd.Timestamp, str] -> start datetime (timestamp or string)
        end: Union[pd.Timestamp, str] = None -> end datetime (timestamp
                or string)
    """
    # fix up the parameters
    method, direction, price_areas, start, end = _rk_nordic_lpi_process_parameters(
        method, direction, price_areas, start, end
    )

    # obtain spot and rk price data from archimedes
    dfspread = _spread_from_rk_data(price_areas, start, end)

    # calculate LPI. Function per method
    if method == "constant_abs":
        df_ret = _rk_nordic_lpi_constant_absolute(dfspread, direction)
    elif method == "constant_perc":
        df_ret = _rk_nordic_lpi_constant_perc(dfspread, direction)

    return df_ret


# -----
# method: constant absolute
# -----
def _rk_nordic_lpi_constant_absolute(
    dfs: pd.DataFrame,
    direction: str,
):
    cutoffs = _get_rk_nordic_constant_cutoffs(dfs.columns, direction)
    dfx = dfs.copy()
    for area in dfs.columns:
        if direction == "up":
            dfx.loc[dfs[area] <= cutoffs[area], area] = 0
            dfx.loc[dfs[area] > cutoffs[area], area] = 1
        else:
            dfx.loc[dfs[area] >= cutoffs[area], area] = 0
            dfx.loc[dfs[area] < cutoffs[area], area] = 1
    return dfx


def _get_rk_nordic_constant_cutoffs(price_areas: list, direction: str):
    """
    Get constant cutoffs stored in the database

    Currently, these are not stored in the DB, so hard coded...
    """
    all_cutoffs_up = {
        "NO1": 20,
        "NO2": 20,
        "NO3": 20,
        "NO4": 20,
        "NO5": 20,
        "SE1": 20,
        "SE2": 20,
        "SE3": 20,
        "SE4": 20,
        "DK1": 20,
        "DK2": 20,
        "FI": 20,
    }
    all_cutoffs_dn = {
        "NO1": -20,
        "NO2": -20,
        "NO3": -20,
        "NO4": -20,
        "NO5": -20,
        "SE1": -20,
        "SE2": -20,
        "SE3": -20,
        "SE4": -20,
        "DK1": -20,
        "DK2": -20,
        "FI": -20,
    }
    if direction == "up":
        all_cutoffs = all_cutoffs_up
    else:
        all_cutoffs = all_cutoffs_dn
    cutoffs = {key: value for key, value in all_cutoffs.items() if key in price_areas}
    return cutoffs


# -----
# method: constant percentage (quantile)
# -----
def _rk_nordic_lpi_constant_perc(
    dfs: pd.DataFrame,
    direction: str,
):
    cutoffs = _get_rk_nordic_perc_cutoffs(dfs.columns)
    dfs = dfs.copy()
    for area in dfs.columns:
        if direction == "up":
            # calc the cut value as quantile (%) of all up regulating prices
            cut = dfs.loc[dfs[area] > 0, area].quantile(q=1 - cutoffs[area])
            dfs.loc[dfs[area] <= cut, area] = 0
            dfs.loc[dfs[area] > cut, area] = 1
        else:
            # calc the cut value as quantile (%) of all dn regulating prices
            cut = dfs.loc[dfs[area] < 0, area].quantile(q=cutoffs[area])
            dfs.loc[dfs[area] < cut, area] = 1
            dfs.loc[dfs[area] >= cut, area] = 0
    return dfs


def _get_rk_nordic_perc_cutoffs(price_areas: list):
    """
    Get percentage cutoffs stored in the database

    Currently, these are not stored in the DB, so hard coded...
    """
    all_cutoffs = {
        "NO1": 0.20,
        "NO2": 0.20,
        "NO3": 0.20,
        "NO4": 0.20,
        "NO5": 0.20,
        "SE1": 0.20,
        "SE2": 0.20,
        "SE3": 0.20,
        "SE4": 0.20,
        "DK1": 0.20,
        "DK2": 0.20,
        "FI": 0.20,
    }
    cutoffs = {key: value for key, value in all_cutoffs.items() if key in price_areas}
    return cutoffs


# -----
# get spread from arcl
# -----
def _spread_from_rk_data(price_areas: list, start: pd.Timestamp, end: pd.Timestamp):
    # read data from archimedes
    df_prices = archimedes.get(
        series_ids=[
            "NP/ConsumptionImbalancePrices",
            "NP/AreaPrices",
            "NP/DominatingDirection",
        ],
        price_areas=price_areas,
        end=end,
        start=start,
    )
    # replace the long series names with short versions
    df_prices.rename(
        columns={
            "NP/AreaPrices": "DAM",
            "NP/ConsumptionImbalancePrices": "rk",
            "NP/DominatingDirection": "direction",
        },
        inplace=True,
    )
    df_prices.index = df_prices.index.tz_convert(PermittedTimeZones.TZ_NORDIC)
    # calc spread and add it in
    df_tmp = df_prices.rk - df_prices.DAM
    # df_tmp.columns = pd.MultiIndex.from_product([["spread"], df_tmp.columns])
    # dfp = df_prices.join(df_tmp)
    return df_tmp


# -----
# process and error check parameters
# -----
def _rk_nordic_lpi_process_parameters(
    method: str,
    direction: str,
    price_areas: Union[list, str],
    start: Union[pd.Timestamp, str],
    end: Union[pd.Timestamp, str],
):
    """
    Process the parameters for rk_nordic_lpi and fix if possible
    """
    # method
    method = _process_param_method(method)
    # direction
    direction = _process_param_direction(direction)
    # price areas
    price_areas = _process_param_price_areas(price_areas)
    # start
    start = _process_param_start(start)
    # end
    end = _process_param_end(end, start)

    return method, direction, price_areas, start, end


def _process_param_method(method):
    """
    process method param
    """
    if isinstance(method, str):
        method = method.lower()
        if method not in LPI_METHODS:
            msg = f"Parameter <method> must be one of {LPI_METHODS}"
            raise ValueError(msg)
    else:
        msg = f"Parameter <method> must be one of {LPI_METHODS}"
        raise ValueError(msg)
    return method


def _process_param_direction(direction):
    """
    process direction param
    """
    if isinstance(direction, str):
        direction = direction.lower()
        if direction == "down":
            direction = "dn"
        if direction not in ["up", "dn"]:
            msg = "Direction parameter must be one of ['up', 'dn']"
            raise ValueError(msg)
    else:
        msg = "Parameter <direction> must be one of ['up', 'dn']"
        raise ValueError(msg)
    return direction


def _process_param_price_areas(price_areas):
    """
    process price_area param
    """
    if isinstance(price_areas, str):
        price_areas = [price_areas]
    if not isinstance(price_areas, list):
        msg = "Parameter <price_areas> must be a string or list"
        # For later - should error check list elements and dim
        raise ValueError(msg)
    return price_areas


def _process_param_start(start):
    """
    process start param
    """
    if isinstance(start, str):
        start = pd.to_datetime(start)
    if not isinstance(start, pd.Timestamp):
        msg = "Parameter <start> must be a time formatted string or a pandas timestamp"
        raise ValueError(msg)
    if start.tzinfo is None:
        start = start.tz_localize(PermittedTimeZones.TZ_NORDIC)
    return start


def _process_param_end(end, start):
    """
    process end param
    """
    if isinstance(end, str):
        end = pd.to_datetime(end)
    if end is None:
        end = pd.Timestamp.today()
    if not isinstance(end, pd.Timestamp):
        msg = "Parameter <end> must be a time formatted string or a pandas timestamp"
        raise ValueError(msg)
    if end.tzinfo is None:
        end = end.tz_localize(PermittedTimeZones.TZ_NORDIC)
    end = max(end, start)
    return end
