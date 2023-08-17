"""
Common helper utilities
"""


def update_fig_traces(fig, trace_update=None):
    """
    Use dict to update figure traces (i.e. existing traces)
    trace_update are arguments for the fig.update_traces function

        Figure.update_traces(patch=None, selector=None, row=None, col=None,
                        secondary_y=None, overwrite=False, **kwargs)
                        → plotly.graph_objects._figure.Figure

        https://plotly.com/python-api-reference/generated/plotly.graph_objects.Figure.html#plotly.graph_objects.Figure.update_traces
    """

    if isinstance(trace_update, dict):
        fig = fig.update_traces(**trace_update)

    return fig
