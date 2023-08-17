import logging
from numbers import Number

import numpy as np
import pandas as pd
import plotly.graph_objects as go

from ..assets import opt_plotly_theme as theme
from ..common.utils import update_fig_traces

logging.basicConfig(level=logging.INFO)


def discrete_distro_bar(
    df_fcast: pd.DataFrame,
    df_obs: pd.DataFrame = None,
    layout_update=None,
    fcast_category_col="direction",
    fcast_value_col="probability",
    obs_value_col="value",
    category_order=None,
    category_direction_map=None,
    trace_update=None,
) -> go.Figure:
    """

    Construct a stacked bar chart for discrete distributions

    Inputs:

    df_fcast -> dataframe for forecasted values, with columns including [from_dt, fcast_category_col, fcast_value_col]
    df_obs -> dataframe with the actual observations, with columns including [from_dt, obs_value_col]

    Note that the df_obs should not have any other data in it - only the observed outturns

    """

    # get the active graph theme (or create one if there isnt one)
    # this way we ensure that these graphs are always formatted with the opt_plotly_theme. yay!
    graph_theme = theme.FabPlotlyTheme()

    # set the graph layout

    layout = _set_layout(layout_update)

    # all nans in the df_obs - just set it to none so it is not graphed
    if df_obs is not None:
        if len(df_obs) >= 1:
            if df_obs[obs_value_col].apply(lambda x: np.isnan(x)).all():
                df_obs = None

    fig = go.Figure(layout=layout)
    if category_order is None:
        category_order = df_fcast[fcast_category_col].unique()
    count = 0
    for cat in category_order:
        df = df_fcast[df_fcast[fcast_category_col] == cat]
        if isinstance(category_direction_map, dict):
            # should check that we have the keys
            direction = category_direction_map[
                cat
            ]  # the direction matching the category
            barcol = graph_theme.direction_hex[
                direction
            ]  # the colour for the direction
        else:
            barcol = graph_theme.pallette[count]
            count = count + 1
        bar = go.Bar(
            x=df.from_dt,
            y=df[fcast_value_col],
            name="{}".format(cat),
            marker_color=barcol,
        )
        fig.add_trace(bar)
    # add a trace for the actual values if they exist
    if df_obs is not None:
        if len(df_obs) > 0:
            fig.add_trace(
                go.Scatter(
                    x=df_obs.from_dt,
                    y=df_obs[obs_value_col],
                    name="Actual",
                    mode="markers",
                )
            )
    # update traces with user defined updates
    fig = update_fig_traces(fig, trace_update)

    return fig


def _set_layout(layout_update):
    """
    Generate the layout object for the graph
    """

    # basic format, to ensure consistency
    layout = go.Layout()

    # specific formatting options for this graph

    layout = layout.update(dict(barmode="stack"))

    layout["yaxis"] = layout["yaxis"].update(
        dict(
            title="Probability",
            showgrid=True,
            range=[0, 1.01],
            # autorange=False
        )
    )

    layout["xaxis"] = layout["xaxis"].update(
        dict(
            hoverformat="%H:%M",
            tickformat="%H",  # %d %B (%a)<br>%Y
            dtick=86400000.0 / 24,
            title=None,
        )
    )

    # update with any user instructions
    if layout_update is not None:
        layout = layout.update(go.Layout(layout_update))

    return layout
