import numpy as np
import pandas as pd
import plotly.graph_objects as go

from ..assets import opt_plotly_theme as theme
from ..common.utils import update_fig_traces


def mirror_bar(
    df_above: pd.DataFrame,
    df_below: pd.DataFrame,
    layout_update=None,
    value_col="indicator",
    above_label="",
    below_label="",
    trace_update=None,
    monochrome=False,
) -> go.Figure:
    """

    Construct a bar chart for two series, where the "above" series is shown above x=0, and the below series is below x=0

    Inputs:

    df_above -> dataframe for above series values, with columns including [from_dt, value_col]
    df_below -> dataframe with the actual observations, with columns including [from_dt, value_col]
    value_col -> the value column name
    above_label, below_label -> labels to use for the two series

    """

    # get the active graph theme (or create one if there isnt one)
    # this way we ensure that these graphs are always formatted with the opt_plotly_theme. yay!
    graph_theme = theme.FabPlotlyTheme()

    # the way this is done is that we use two axes - one for the above, one for the below

    # set the graph layout

    layout = _set_layout(above_label, below_label, layout_update)

    # create the figure and add a series for each category

    fig = go.Figure(layout=layout)

    if len(df_above) > 0:
        above_bar = go.Bar(
            x=df_above.from_dt,
            y=df_above[value_col],
            name="{}".format(above_label),
        )
        # above_bar.update(marker_color=graph_theme.element_colours["bar_above"])

        fig.add_trace(above_bar)

    if len(df_below) > 0:
        df_b = df_below.copy()
        df_b[value_col] = df_b[value_col]
        below_bar = go.Bar(
            x=df_b.from_dt,
            y=df_b[value_col],
            xaxis="x",
            yaxis="y2",
            name="{}".format(below_label),
        )
        # below_bar.update(marker_color=graph_theme.element_colours["bar_below"])

        fig.add_trace(below_bar)

    # if monochrome update all traces to monochrome colour
    if monochrome == True:
        col = graph_theme.monochrome_hex
        fig.update_traces(patch={"marker_color": col})

    # update traces with user defined updates
    fig = update_fig_traces(fig, trace_update)

    return fig


def _set_layout(above_label, below_label, layout_update):
    """
    Generate the layout object for the graph
    """

    # basic format, to ensure consistency
    layout = go.Layout()

    # specific formatting options for this graph

    layout = layout.update(dict(barmode="overlay"))

    layout["yaxis"] = layout["yaxis"].update(
        dict(
            title="{}   ←   Index   →   {}".format(below_label, above_label),
            showgrid=True,
            range=[-10.01, 10.01],
            tickmode="array",
            tickvals=list(range(-10, 11, 2)),
            ticktext=[str(abs(i)) for i in list(range(-10, 11, 2))],
        )
    )

    layout["yaxis2"] = dict(
        title=None,
        range=[10.01, -10.01],
        # autorange="reversed",
        # fixedrange=True,
        anchor="x",
        overlaying="y",
        visible=False,
        side="right",
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
