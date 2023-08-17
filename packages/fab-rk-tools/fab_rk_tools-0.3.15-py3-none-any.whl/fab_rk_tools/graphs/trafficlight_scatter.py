from enum import Enum

# import fab_rk_tools.assets.plotly_theme as theme
# from ..assets import plotly_theme as theme
from importlib import reload
from math import floor

import numpy as np
import pandas as pd
import plotly.graph_objects as go

import fab_rk_tools.assets.opt_plotly_theme as theme
from fab_rk_tools.common.utils import update_fig_traces


def trafficlight_scatter(
    df, layout_update=None, value_col="marker", marker_size=20, trace_update=None
):
    """
    Traffic light scatter plot. Graphs a coloured circle (marker) per point, where the colours are specified in the input
    dataframe ("RED", "GREEN" etc). The colour definitions are taken from a opt plotly theme object.

    """

    # Expanded plotly theme. If one is instansiated, then load it otherwise create one and use the default
    graph_theme = theme.FabPlotlyTheme()
    colours = graph_theme.hex_to_rgb(graph_theme.trafficlight_hex)

    # fix layout
    layout = _set_layout(layout_update)

    # new figure
    fig = go.Figure(layout=layout)

    # specify marker colours for each point, in a df
    marker_colours = _prepare_marker_colours(df, value_col, colours)

    # marker line size
    line_size = max(1, floor(marker_size / 3))

    # add the trace for the graph

    fig.add_trace(
        go.Scatter(
            x=marker_colours.from_dt,
            y=np.zeros(len(marker_colours)),
            mode="markers",
            marker=dict(
                color=list(marker_colours.marker_rgb),
                symbol="circle",
                size=marker_size,
                line=dict(color=list(marker_colours.marker_rgba), width=line_size),
            ),
            showlegend=False,
            # hoverinfo='none'
        ),
    )

    # update traces with user defined updates
    fig = update_fig_traces(fig, trace_update)

    return fig


def _set_layout(layout_update):
    """
    Generate the layout object for the graph
    """

    # basic layout, before adjustments
    layout = go.Layout(
        yaxis=dict(
            range=[-1, 1],
            showgrid=False,
            zeroline=False,
            visible=False,
            fixedrange=True,
        ),
        height=140,
        hovermode=False,
    )

    layout["xaxis"] = layout["xaxis"].update(
        dict(
            hoverformat="%H:%M",
            tickformat="%H",  # %d %B (%a)<br>%Y
            dtick=86400000.0 / 24,
            title=None,
            fixedrange=True,
        )
    )

    # hovertext
    layout["hoverlabel"] = dict(
        font_size=10,
    )

    # update with any user instructions
    if layout_update is not None:
        layout = layout.update(go.Layout(layout_update))

    return layout


def _make_transparent(rgb, opacity=0.7):
    """
    make the rgb string into a transparent rgb string
    """
    return f"rgba{rgb[3:-1]}, {opacity})"


def _prepare_marker_colours(df_data, value_col, colours, opacity=0.7):
    """
    Calculate the line and fill marker colours for each row in srs
    """

    # create dataframe for results
    df = df_data[["from_dt", value_col]]

    m_solid = "marker_rgb"
    m_transparent = "marker_rgba"

    if "default" in colours:
        default_colour = colours["default"]
    else:
        default_colour = list(colours.values())[0]
    # marker & line colours
    df.loc[:, m_solid] = default_colour  # default to default colour
    df.loc[:, m_transparent] = _make_transparent(
        default_colour, opacity
    )  # default to default colour

    for colour, rgb in colours.items():
        if colour != "default":
            df.loc[df[value_col] == colour, m_solid] = rgb
            df.loc[df[value_col] == colour, m_transparent] = _make_transparent(
                rgb, opacity
            )
    return df
