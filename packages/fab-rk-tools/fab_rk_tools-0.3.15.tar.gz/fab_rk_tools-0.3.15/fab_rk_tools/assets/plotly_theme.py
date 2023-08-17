import plotly.graph_objects as go
import plotly.io as pio

# ______________________________________
# Define themes
# ______________________________________
#

DEFAULT_THEME = "dark"

# Themes are defined globally

_theme_def = dict()
_theme_pallette = dict()
_theme_element_colours = dict()
_theme_trafficlight = dict()

#
# Dark theme pallette and element colours
#

_theme_def["dark"] = "plotly_dark"

_theme_pallette["dark"] = [
    "#ff707a",
    "#ab82e0",
    "#008fd1",
    "#ffa600",
    "#688ce1",
    "#ff6aa8",
    "#e374cc",
    "#ff8749",
]

_theme_trafficlight["dark"] = dict(
    GREEN="rgb(74,163,44)",
    YELLOW="rgb(255,200,32)",
    RED="rgb(174,32,18)",
    default="rgb(226,205,141)",
)

_theme_element_colours["dark"] = dict(
    bar_below="#BF481D",
    bar_above="#7CB259",
    app_background="#222",
    text="#fafafa",
    # box_background= "#303030",
    box_background="#262730",
    axis="#fafafa",
    axis_line="#fafafa",
    grid_line="#777777",
    spikes="#97aec2",
    pallette=_theme_pallette["dark"],
    rangeslider_border="#b1c3d4",
    rangeslider_bg="#444",
    now_line="#AAAAAA",
    button_bg="#444",
    button_bg_focus="#28415b",
    endpoint_colour=_theme_pallette["dark"][1],
    bar_marker_line="#AAAAAA",
    bar_marker_line_highlight="orange",
    table_odd_row="#555",
    table_even_row="#555",
    table_firstcol_odd="#555",
    table_firstcol_even="#555",
    table_header="#444",
    table_border="#303030",
)

#
# light theme pallette and element colours
#

_theme_def["light"] = "plotly"
_theme_pallette["light"] = ["#dd7230", "#2e1f27", "#009ec2", "#ecd444", "#90708c"]

_theme_trafficlight["light"] = _theme_trafficlight["dark"].copy()

_theme_element_colours["light"] = dict(
    bar_below="#BF481D",
    bar_above="#7CB259",
    app_background="#FFFFFF",
    text="#25211E",
    box_background="#F2F2F2",
    axis="#25211E",
    axis_line="#25211E",
    grid_line="#70645B",
    spikes="#70645B",
    now_line="#70645B",
    pallette=_theme_pallette["light"],
    rangeslider_border="#b1c3d4",
    rangeslider_bg="#444",
    button_bg="#444",
    button_bg_focus="#28415b",
    endpoint_colour=_theme_pallette["light"][1],
    bar_marker_line="#AAAAAA",
    bar_marker_line_highlight="orange",
    table_odd_row="#555",
    table_even_row="#555",
    table_firstcol_odd="#555",
    table_firstcol_even="#555",
    table_header="#444",
    table_border="#303030",
)

# ______________________________________
# Define structure
# ______________________________________
#
# Structure (margins etc) is defined globally

# plot margins
_plot_margins_default = dict(l=50, r=50, b=50, t=50, pad=4)

_plot_margins_streamlit = dict(l=5, r=5, b=5, t=5, pad=1)

_table_structure_default = dict(
    width_firstcol=3,
    width_col=1,
    cell_height=30,
    line_width=2,
    outer_margins=dict(l=20, r=20, b=50, t=50, pad=4),
)

# ______________________________________
# Define legends
# ______________________________________
#
# Legend options are defined globally
# These should be accessed directly by the user/graph functions
_legend_layout = dict()
_legend_layout["right_vertical"] = go.Layout(
    legend=dict(
        orientation="v", yanchor="top", xanchor="left", x=1.02, y=1, font=dict(size=12)
    )
)

_legend_layout["top_right_horizontal"] = go.Layout(
    legend=dict(
        orientation="h",
        yanchor="bottom",
        xanchor="right",
        x=1.02,
        y=1,
        font=dict(size=12),
    )
)

_legend_layout["bottom_centre_horizontal"] = go.Layout(
    legend=dict(
        orientation="h",
        yanchor="top",
        xanchor="center",
        x=0.5,
        y=-0.1,
        font=dict(size=12),
    )
)

# ______________________________________
# Theme class
# ______________________________________
#


class FabPlotlyTheme:
    def __init__(self, graphformat, legendlayout=None, theme=None):
        theme = theme.lower()
        graphformat = graphformat.lower()

        # availble stuff

        self.available_themes = list(_theme_def.keys())
        self.available_legend_layouts = list(_legend_layout.keys())

        # make sure legal theme
        if theme is None:
            theme = self.available_themes[0]
        elif theme not in self.available_themes:
            msg = "Invalid theme provided. Cannot initialise."
            raise ValueError(msg)

        # initialise plotly templates (themes)
        for t, base in _theme_def.items():
            self._theme_formatting(t, base)

        # set theme
        self.set_plotly_theme(theme)

        # set graph format
        self.set_default_graph_format(graphformat=graphformat)

        # set default legend layout
        self.set_default_legend_layout(legendlayout)

    def set_plotly_theme(self, theme=None):
        """
        Set the default theme to use for plotly graphs
        """

        # make sure legal theme
        if theme is None:
            theme = self.available_themes[0]
        else:
            theme = theme.lower()

        if theme not in self.available_themes:
            msg = "Invalid theme provided. Cannot set plotly theme."
            raise ValueError(msg)
        pio.templates.default = theme
        self.active_theme = theme
        self.pallette = _theme_pallette[theme]
        self.element_colours = _theme_element_colours[theme]
        self.trafficlight = _theme_trafficlight[theme]
        # need to redefine the graph formats so they have the right paper colours
        self._set_graph_formats()
        # set legend layouts
        self.legend_layout = _legend_layout

    def set_default_graph_format(self, graphformat):
        """
        Set the (default) graph format (size etc)
            format => ["standard", "large"]

        You can choose to override these by specifying the formats for specific graphs

        """
        if graphformat is None:
            graphformat = self.available_graph_formats[0]
        else:
            graphformat = graphformat.lower()
        if graphformat not in self.available_graph_formats:
            msg = f"Invalid graph format provided"
            raise ValueError(msg)
        self.default_graph_format = self.graph_format[graphformat]

    def set_default_legend_layout(self, legendlayout=None):
        """
        Set the (default) legend layout (position etc)
            format => ["standard", "large"]

        You can choose to override these by specifying the formats for specific graphs

        """

        if legendlayout is None:
            legendlayout = "right_vertical"
        else:
            legendlayout = legendlayout.lower()
        if legendlayout not in self.available_legend_layouts:
            msg = f"Invalid graph format provided"
            raise ValueError(msg)
        self.default_legend_layout = _legend_layout[legendlayout]

    # ______________________________________
    # General layout formatting
    # ______________________________________

    def _theme_formatting(self, theme, base_theme):
        # make sure legal theme
        if theme not in self.available_themes:
            msg = "Invalid theme provided. Cannot initialise."
            raise ValueError(msg)

        pio.templates[theme] = pio.templates[base_theme]
        this_theme = pio.templates[theme]
        this_element_colours = _theme_element_colours[theme]

        # plot background
        this_theme["layout"]["paper_bgcolor"] = this_element_colours["box_background"]
        this_theme["layout"]["plot_bgcolor"] = this_element_colours["box_background"]

        # axes. Here use the color property to set everything at once. Maybe control finer later.
        this_theme["layout"]["xaxis"]["color"] = this_element_colours["axis"]
        this_theme["layout"]["yaxis"]["color"] = this_element_colours["axis"]
        this_theme["layout"]["xaxis"]["linecolor"] = this_element_colours["axis"]
        this_theme["layout"]["yaxis"]["linecolor"] = this_element_colours["axis"]
        this_theme["layout"]["xaxis"]["linewidth"] = 1
        this_theme["layout"]["yaxis"]["linewidth"] = 1
        this_theme["layout"]["xaxis"]["showline"] = True
        this_theme["layout"]["yaxis"]["showline"] = True
        this_theme.layout.xaxis.type = "-"

        # xaxis rangeslider formatting
        this_theme.layout.xaxis.rangeslider.visible = False
        this_theme.layout.xaxis.rangeslider.borderwidth = 0
        this_theme.layout.xaxis.rangeslider.bordercolor = this_element_colours[
            "rangeslider_border"
        ]
        this_theme.layout.xaxis.rangeslider.thickness = 0.20
        this_theme.layout.xaxis.rangeslider.bgcolor = this_element_colours[
            "rangeslider_bg"
        ]

        # xaxis rangeselector formatting
        this_theme.layout.xaxis.rangeselector.visible = False
        this_theme.layout.xaxis.rangeselector.font.color = this_element_colours["text"]
        this_theme.layout.xaxis.rangeselector.bgcolor = this_element_colours[
            "button_bg"
        ]
        this_theme.layout.xaxis.rangeselector.activecolor = this_element_colours[
            "button_bg"
        ]
        this_theme.layout.xaxis.rangeselector.borderwidth = 0

        # axis spikes
        this_theme["layout"]["yaxis"]["showspikes"] = False
        this_theme["layout"]["xaxis"]["showspikes"] = True
        this_theme["layout"]["xaxis"]["spikethickness"] = 1
        this_theme["layout"]["xaxis"]["spikedash"] = "dot"
        this_theme.layout.xaxis.spikesnap = "data"
        this_theme["layout"]["xaxis"]["spikecolor"] = this_element_colours["spikes"]
        this_theme.layout.spikedistance = 5000

        # grid
        this_theme["layout"]["yaxis"]["gridcolor"] = this_element_colours["grid_line"]
        this_theme["layout"]["yaxis"]["showgrid"] = True
        this_theme["layout"]["xaxis"]["showgrid"] = False

        # get rid of zerolines
        this_theme["layout"]["xaxis"]["zeroline"] = False
        this_theme["layout"]["yaxis"]["zeroline"] = False

        # margin
        # this_theme.layout.margin = _plot_margins_default
        this_theme.layout.margin = _plot_margins_default

        # hover
        this_theme.layout.hovermode = "x"
        this_theme.layout.xaxis.hoverformat = "%{x:.2f}"
        this_theme.layout.hoverdistance = 100

        # graph series colours
        this_theme.layout.colorway = this_element_colours["pallette"]

        # Plot-type specific formatting

        # scatter plots
        this_theme.data.scatter = [
            go.Scatter(
                hovertemplate="%{y:.2f}",
                line=dict(shape="linear", dash="solid", width=1),
            )
        ]

        # bar plots
        # this_theme.layout.barmode='stack'
        this_theme.layout.bargap = 0.1
        this_theme.data.bar = [
            go.Bar(
                # hovertemplate="%{y:.2f}<extra></extra>",
                hovertemplate="%{y:.2f}",
                marker=dict(opacity=0.9, line={"width": 1}),
            )
        ]

        # tables
        this_theme.data.table = [go.Table(hoverinfo="x+y")]

    # ______________________________________
    # Graph formats
    # ______________________________________
    #
    # These are NOT defined as globals, as we have to overwrite the paper colours
    # if we update the theme (as streamlit will overwrite them otherwise)

    def _set_graph_formats(self):
        self.graph_format = dict()
        this_element_colours = _theme_element_colours[self.active_theme]

        self.graph_format["standard"] = go.Layout(
            # height = 300,
            xaxis=dict(tickfont={"size": 12}, titlefont={"size": 12}),
            yaxis=dict(tickfont={"size": 12}, titlefont={"size": 12}),
            # have to explicitly specify the paper colours since streamlit overwrites the theme
            # paper_bgcolor=this_element_colours["box_background"],
            # plot_bgcolor=this_element_colours["box_background"]
        )

        self.graph_format["large"] = go.Layout(
            height=350,
            xaxis=dict(tickfont={"size": 12}, titlefont={"size": 12}),
            yaxis=dict(tickfont={"size": 12}, titlefont={"size": 12}),
            # have to explicitly specify the paper colours since streamlit overwrites the theme
            # paper_bgcolor=this_element_colours["box_background"],
            # plot_bgcolor=this_element_colours["box_background"]
        )

        self.available_graph_formats = self.graph_format.keys()
