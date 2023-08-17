"""
Unit tests for derived data
"""
import pandas as pd
import pytest

from ...common.constants import PermittedTimeZones
from ..deriveddata import _rk_nordic_lpi_process_parameters


@pytest.fixture
def legal_parameters():
    """
    Legal set of parameters for the rk_nordic_lpi function
    """

    p_in = {
        "method": "constant_abs",
        "direction": "UP",
        "price_areas": ["NO1", "NO2"],
        "start": "2022-03-02",
        "end": pd.to_datetime("2022-04-01 04:00:00").tz_localize(
            PermittedTimeZones.TZ_NORDIC
        ),
    }
    p_out = p_in.copy()
    p_out["direction"] = p_out["direction"].lower()
    p_out["start"] = pd.to_datetime(p_out["start"]).tz_localize(
        PermittedTimeZones.TZ_NORDIC
    )
    return [p_in, p_out]


def test_parameters(legal_parameters):
    """
    Test error checking of rk_nordic_lpi function parameters
    """

    # pylint: disable=redefined-outer-name

    test_out = _rk_nordic_lpi_process_parameters(**legal_parameters[0])
    assert test_out == tuple(legal_parameters[1].values())
