import numpy as np
import pandas as pd
import plotly.graph_objects as go
from pyparsing import col

from ..assets import opt_plotly_theme as theme
from ..common.utils import update_fig_traces


def basic_bar(
    df: pd.DataFrame,
    layout_update=None,
    series_cols=["price"],
    yaxis_label=None,
    y_scale=None,
    trace_update=None,
    monochrome=False,
) -> go.Figure:
    """

    Construct a bar chart for series provided in the dataframe.
    The series are provided as columes in the dataframe

    Inputs:

    df -> dataframe for series values, with columns including [from_dt, series_cols]
    series_cols -> list, the columns in df for the series to graph
    labels -> list, display labels to use for the series
    colour_ids -> list, colours to use for hte series

    """

    # get the active graph theme (or create one if there isnt one)
    # this way we ensure that these graphs are always formatted with the opt_plotly_theme. yay!
    graph_theme = theme.FabPlotlyTheme()

    _error_check(df, series_cols, yaxis_label, y_scale)

    # the way this is done is that we use two axes - one for the above, one for the below

    # set the graph layout

    layout = _set_layout(
        yaxis_label=yaxis_label, y_scale=y_scale, layout_update=layout_update
    )

    # create the figure and add a series for each category

    fig = go.Figure(layout=layout)

    for s in series_cols:
        new_bar = go.Bar(
            x=df.from_dt,
            y=df[s],
            name=f"{s}",
            # marker_color = theme.pallette_theme[above_colour_id],
        )
        fig.add_trace(new_bar)

    if len(series_cols) == 1:
        # remove series name from hover
        fig.update_traces(hovertemplate="%{y:.2f}<extra></extra>")

    # if monochrome update
    if monochrome == True:
        col = graph_theme.monochrome_hex
        fig.update_traces(patch={"marker_color": col})

    # update traces with user defined updates
    fig = update_fig_traces(fig, trace_update)
    return fig


def _error_check(df, series_cols, yaxis_label, y_scale):
    if not isinstance(series_cols, list):
        msg = "Series_cols need to be provided as a list"
        raise ValueError(msg)
    if not (isinstance(yaxis_label, str) or yaxis_label is None):
        msg = "yaxis_label needs to be None or a string"
        raise ValueError(msg)
    if not isinstance(df, pd.DataFrame):
        msg = "df must be a dataframe"
        raise ValueError(msg)
    if not (isinstance(y_scale, list) or y_scale is None):
        msg = "y_scale needs to be provided as a list"
        raise ValueError(msg)

    if not (set(series_cols) <= set(df.columns)):
        msg = (
            "Provided column list in series_cols is not found in the dataframe columns"
        )
        raise ValueError(msg)
    if y_scale is not None and (len(y_scale) < 2 or len(y_scale) > 3):
        msg = "y_scale needs 2 or 3 elements"
        raise ValueError(msg)


def _set_layout(yaxis_label, layout_update, y_scale=None, barmode="group"):
    """
    Generate the layout object for the graph
    """

    # basic format
    layout = go.Layout()

    # specific formatting options for this graph
    layout = layout.update(dict(barmode=barmode))

    layout["yaxis"] = layout["yaxis"].update(
        dict(
            title=f"{yaxis_label}",
            showgrid=True,
        )
    )
    if y_scale is not None:
        layout["yaxis"] = layout["yaxis"].update(dict(range=y_scale))

    layout["xaxis"] = layout["xaxis"].update(
        dict(
            hoverformat="%H:%M",
            tickformat="%H",  # %d %B (%a)<br>%Y
            dtick=86400000.0 / 24,
            title=None,
        )
    )

    # update with any user graph formatting instructions
    if layout_update is not None:
        layout = layout.update(go.Layout(layout_update))

    return layout
