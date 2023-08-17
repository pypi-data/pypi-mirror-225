import numpy as np
import pandas as pd
import plotly.graph_objects as go

from ..assets import opt_plotly_theme as theme

# import plotly.io as pio
from ..common.utils import update_fig_traces


def scatter_quantile_fan(
    df_q: pd.DataFrame,
    df_l: pd.DataFrame,
    quantile_col="quantile",
    quantile_value="value",
    series_col="series",
    series_value="value",
    layout_update=None,
    trace_update=None,
    monochrome=False,
) -> go.Figure:
    """

    Construct a scatter fan diagram

    Inputs:

    df_q -> dataframe for quantiles, with columns [from_dt, ref_dt, quantile, value]
    df_l -> dataframe for all other data to graph, with columns [from_dt, series, value]

    The function will graph df_q between min and max quantiles, and the median (0.5) quantile, as a fan
    Each series in df_l will be graphed as a line

    """

    # get the active graph theme (or create one if there isnt one)
    graph_theme = theme.FabPlotlyTheme()

    # test params
    _scatter_quantile_fan_error_test(df_q, df_l)

    # extract the quantiles
    quantiles = list(df_q[quantile_col].unique())
    qmax = max(quantiles)
    qmin = min(quantiles)
    qmed = _find_middle(quantiles)

    # Create a df for min, max, med. Just makes the graph code slightly easier to read
    df_min = df_q[(df_q[quantile_col] == qmin)].copy()
    df_max = df_q[(df_q[quantile_col] == qmax)].copy()
    df_med = df_q[(df_q[quantile_col] == qmed)].copy()

    # define the graph with our scatter fan layout
    fig = go.Figure(layout=_scatter_quantile_fan_layout(layout_update))

    # copy the colour palette for graphs
    palette_colors = list(graph_theme.pio_default_template().layout.colorway)

    # first the fan colour. We want this to be semi-transparent and the same colour as the first trace
    # get the first colour in the colorway for the active (default) template

    if monochrome:
        fan_col_base = graph_theme.monochrome_hex
    else:
        fan_col_base = graph_theme.fan_hex
    h = fan_col_base.lstrip("#")
    fan_col_rgb_transp = list(int(h[i : i + 2], 16) for i in (0, 2, 4))
    fan_col_rgb_transp.append(0.3)
    fan_col_rgb_transp = "rgba" + str(tuple(fan_col_rgb_transp))

    # upper and lower lines for the fan. set to be 100% transparent
    fan_border_line = dict(color="rgba(0,0,0,0)")

    # add the quantile fan
    name = str(qmin * 100) + "%"
    label = name
    fig.add_trace(
        go.Scatter(
            y=df_min[quantile_value],
            x=df_min.from_dt,
            name=name,
            mode="lines",
            line=fan_border_line,
            showlegend=False,
            hovertemplate=label + ": %{y:.2f}<extra></extra>",
        )
    )

    name = str(qmin * 100) + "%-<br>" + str(qmax * 100) + "%"
    label = str(qmax * 100) + "%"
    fig.add_trace(
        go.Scatter(
            y=df_max[quantile_value],
            x=df_max.from_dt,
            fill="tonexty",
            fillcolor=fan_col_rgb_transp,
            mode="lines",
            line=fan_border_line,
            name=name,
            hovertemplate=label + ": %{y:.2f}<extra></extra>",
        )
    )

    name = str(qmed * 100) + "%"
    label = name
    fig.add_trace(
        go.Scatter(
            y=df_med[quantile_value],
            x=df_med.from_dt,
            name=name,
            mode="lines+markers",
            hovertemplate=label + ": %{y:.2f}<extra></extra>",
            marker=dict(symbol="circle", opacity=0.5, size=8, color=fan_col_base),
            line=dict(color=fan_col_base),
        )
    )

    # add the lines for the market prices if we have them
    # remove the fan colour if it is there
    palette_colors = [
        palette_color
        for palette_color in palette_colors
        if palette_color != fan_col_base
    ]
    if len(df_l) > 0:
        series = list(df_l[series_col].unique())
        for s in series:
            # cycle through the colourway like plotly normally does, but skipping fan colour
            # so other data is never the same colour as the quantile fan
            srs_col = palette_colors[series.index(s) % len(palette_colors)]
            df_x = df_l[df_l[series_col] == s]
            # format the marker
            line = dict(
                color=srs_col,
                width=1,
            )
            marker = dict(symbol="circle", color=srs_col, opacity=0.5, size=8)
            fig.add_trace(
                go.Scatter(
                    y=df_x[series_value],
                    x=df_x.from_dt,
                    name=str(s),
                    mode="lines+markers",
                    line=line,
                    marker=marker,
                    hovertemplate=str(s) + ": %{y:.2f}<extra></extra>",
                )
            )

    # if monochrome update all traces to monochrome colour
    if monochrome == True:
        col = graph_theme.monochrome_hex
        fig.update_traces(patch={"marker_color": col, "line_color": col})

    # update traces with user defined updates
    fig = update_fig_traces(fig, trace_update)

    # add vertical line
    ref_dt = pd.to_datetime(df_q.ref_dt.unique()[0])
    trace_col = graph_theme.pio_default_template().layout.yaxis.gridcolor
    fig.add_trace(_scatter_now_line(ref_dt, trace_col))  # temp - fix this
    return fig


def _find_middle(input_list):
    input_list = sorted(input_list)
    middle = float(len(input_list)) / 2
    if middle % 2 != 0:
        return input_list[int(middle - 0.5)]
    else:
        return (input_list[int(middle)], input_list[int(middle - 1)])


def _scatter_quantile_fan_error_test(df_q, df_l) -> bool:
    """
    Perform error checking. Raise error if not ok
    """
    # extract the quantiles
    quantiles = df_q["quantile"].unique()

    # quantiles
    # if len(quantiles)!=3:
    #    msg = "Expected to receive 3 quantiles to graph - a high, low and medium (or equivalent). Received instead: {}".format(quantiles)
    #    raise ValueError(msg)
    if not is_numeric(quantiles):
        msg = "Expected quantiles to be numeric quantiles (check - are they string or simuilar?)"
        raise ValueError(msg)
    if not is_fraction(quantiles):
        msg = "Expected fractional quantiles. Received {}".format(quantiles)
        raise ValueError(msg)

    # ref_dt
    ref_dt = df_q.ref_dt.unique()
    if len(ref_dt) > 1:
        msg = (
            "Expected only one ref_dt for the prediction quantiles. Received {}".format(
                ref_dt
            )
        )
        raise ValueError(msg)


def _scatter_quantile_fan_layout(layout_update) -> dict:
    """
    Return a layout dict for the figure
    """
    # default
    layout = go.Layout()

    layout["yaxis"] = {"title": "€/MWh"}

    # add the vertical nowline
    layout["yaxis2"] = {
        "anchor": "x",
        "fixedrange": True,
        "overlaying": "y",
        "range": [0, 1],
        "side": "right",
        "visible": False,  # The secondary yaxis is invisible
    }

    layout["xaxis"] = layout["xaxis"].update(
        dict(
            hoverformat="%H:%M",
            tickformat="%H",  # %d %B (%a)<br>%Y
            dtick=86400000.0 / 24,
            title=None,
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


def _scatter_now_line(ref_dt, colour):
    nowline = go.Scatter(
        x=[ref_dt, ref_dt],
        y=[0, 1],
        mode="lines",
        line=dict(shape="linear", width=1, dash="dot", color=colour),
        showlegend=False,
        xaxis="x",
        yaxis="y2",
        name="fcast built",
        hoverinfo="skip",
        hovertemplate="",
    )
    return nowline


def is_numeric(obj):
    try:
        obj + obj, obj - obj, obj * obj, obj**obj, obj / obj
    except ZeroDivisionError:
        return True
    except Exception:
        return False
    else:
        return True


def is_fraction(alist):
    for l in alist:
        if l > 1:
            return False
        if l < 0:
            return False
    return True
