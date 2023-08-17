"""
docstring
"""
import json
import logging

import pandas as pd
import plotly.io as pio

logging.basicConfig(level=logging.INFO)

# ______________________________________
# Define themes
# ______________________________________
#

DEFAULT_COLOUR_THEME = "dark"
DEFAULT_DESIGN_THEME = "optidesign"
DEFAULT_PIO_THEME = "plotly_dark"  # base theme from pio to base everything on
OPTIMEERING_THEME = "optitheme"  # name to use in pio. Doesn't matter what it is.

# defaul theme definition

DEFAULT_COLOUR_THEME_JSON = """{
    "colors": [
        {"name":"blue_dark","hex":"#415B8C","rgb":"65, 91, 140"},
        {"name":"blue_mid","hex":"#799BD9","rgb":"121, 155, 217"},
        {"name":"blue_light","hex":"#BFCFED","rgb":"191, 207, 237"},
        {"name":"lime_light","hex":"#B5D964","rgb":"181, 217, 100"},
        {"name":"green_mid","hex":"#9CB36B","rgb":"119, 140, 72"},
        {"name":"green_dark","hex":"#778C48","rgb":"119, 140, 72"},
        {"name":"dusky_light","hex":"#D99A8F","rgb":"217, 154, 143"},
        {"name":"dusky_mid","hex":"#C15B49","rgb":"137, 60, 47"},
        {"name":"dusky_dark","hex":"#A74A39","rgb":"137, 60, 47"},
        {"name":"yellow_mid","hex":"#F6DE50","rgb":"137, 60, 47"},
        {"name":"blue_very_dark","hex":"#0D121C","rgb":"13, 18, 28"},
        {"name":"off_white","hex":"#F7F8FA","rgb":"247, 248, 250"}
    ],
    "roles": {
        "box_background": "blue_very_dark",
        "primary_text": "off_white",
        "graph_sequence": ["blue_mid", "lime_light", "dusky_light", "green_dark", 
            "blue_light", "dusky_dark", "blue_dark"],
        "axis": "off_white",
        "grid_line": "off_white",
        "spikes": "off_white",
        "trafficlight": {
            "GREEN": "green_mid",
            "YELLOW": "yellow_mid",
            "RED": "dusky_dark",
            "default": "blue_mid"
        }
    }
    
}"""

# default theme structure JSON

DEFAULT_DESIGN_THEME_JSON = """
{
    "layout": {
        "height": 350, 
        "xaxis": {
            "tickfont": {
                "size": 12
            },
            "titlefont": {
                "size": 12
            }, 
            "linewidth": 1, 
            "showline": true, 
            "type": "-", 
            "showspikes": true, 
            "spikethickness": 1, 
            "spikedash": "dot", 
            "spikesnap": "data", 
            "showgrid": false, 
            "zeroline": false, 
            "hoverformat": "%{x:.2f}"
        }, 
        "yaxis": {
            "tickfont": {
                "size": 12
            }, 
            "titlefont": {
                "size": 12
            }, 
            "linewidth": 1, 
            "showline": true, 
            "showspikes": false, 
            "showgrid": true, 
            "zeroline": false,
            "nticks": 8
        }, 
        "spikedistance": 5000, 
        "bargap": 0.1, 
        "margin": {
            "l": 50, 
            "r": 50, 
            "b": 50, 
            "t": 50,
            "pad": 4
        }, 
        "hovermode": "x", 
        "hoverdistance": 100, 
        "legend": {
            "orientation": "v", 
            "yanchor": "top", 
            "xanchor": "left", 
            "x": 1.02, 
            "y": 1, 
            "font_size": 12
        }
    },
    "data": {
        "bar": {
            "hovertemplate": "%{y:.2f}",
            "marker": {
                "opacity": 0.9,
                "line": {
                    "width": 1
                }
            }
        },
        "table": {
            "hoverinfo": "x+y"
        },
        "scatter": {
            "hovertemplate":"%{y:.2f}",
            "line": {
                "shape": "linear",
                "dash": "solid",
                "width": 1
            }
        }
    }
}
"""
# ______________________________________
# Theme class
# ______________________________________
#


class FabPlotlyTheme:
    """
    Depreciated FabPLotlyTheme - do not use this. Rather import opt_plotly_theme instead
    """

    # pylint: disable=too-many-instance-attributes

    def __init__(
        self, colour_theme=None, design_theme_adjustments=None, base_theme=None
    ):
        logging.warning(
            (
                "plotly_theme is depreciated, and will be removed in an upcoming "
                "version of fab_rk_tools. Use opt_plotly_theme instead."
            )
        )

        # actives are none at start
        self.active_base_theme = None
        self.active_colour_theme = None
        self.active_design_theme_adjustments = None
        self._colour_theme_dict = None
        self._colour_theme_json = None
        self._colour_theme_name = None
        self._colours_df = None
        self._colours_graph = None
        self._colours_trafficlight_hex = None
        self._colours_trafficlight_rgb = None
        self._colours_elements = None
        self._design_theme_dict = None
        self._design_theme_json = None
        self._design_theme_name = None
        self._colours_graphs = None

        # load the inbuilt colour and design adjustment themes
        self._colour_theme_json = {}
        self._design_theme_json = {}
        # availble stuff
        self.available_colour_themes = []
        self.available_design_theme_adjustments = []
        # load the defaults so we have at least these
        self.load_colour_theme(
            colour_theme=DEFAULT_COLOUR_THEME,
            colour_theme_json=DEFAULT_COLOUR_THEME_JSON,
        )
        self.load_design_theme_adjustments(
            design_theme=DEFAULT_DESIGN_THEME,
            design_theme_json=DEFAULT_DESIGN_THEME_JSON,
        )

        # set themes to defualts if none selected
        if colour_theme is None:
            colour_theme = DEFAULT_COLOUR_THEME
        if design_theme_adjustments is None:
            design_theme_adjustments = DEFAULT_DESIGN_THEME

        # activate the theme, using the defualts where these are not selected

        self.activate_theme(
            colour_theme=colour_theme,
            design_theme_adjustments=design_theme_adjustments,
            base_theme=base_theme,
        )

    def load_colour_theme(self, colour_theme, colour_theme_json):
        """
        Load in a new colour theme

        colour_theme_name: str, name of the new theme
        colour_theme_json: json, json definition of the theme colours.

        """

        # at some stage we shoudl error check the json
        self._colour_theme_json[colour_theme] = colour_theme_json
        # availble stuff
        self.available_colour_themes.append(DEFAULT_COLOUR_THEME)

    def load_design_theme_adjustments(self, design_theme, design_theme_json):
        """
        docstring
        """
        self._design_theme_json[design_theme] = design_theme_json
        # availble stuff
        self.available_design_theme_adjustments.append(DEFAULT_DESIGN_THEME)

    def _set_colour_theme(self, colour_theme):
        """
        Set one of the loaded colour themes to be the colour theme we use
        """
        # make sure legal colour theme
        if colour_theme is None:
            colour_theme = DEFAULT_COLOUR_THEME
        colour_theme = colour_theme.lower()

        if colour_theme not in self.available_colour_themes:
            msg = "Invalid colour theme provided. Cannot set plotly colour theme."
            raise ValueError(msg)

        # convert colour theme json to dict
        self._colour_theme_name = colour_theme
        self._colour_theme_dict = json.loads(self._colour_theme_json[colour_theme])

        # store colours in a dataframe
        self._colours_df = pd.DataFrame(self._colour_theme_dict["colors"])
        self._colours_df = self._colours_df.set_index("name")

        # set up a list with graph colours in order
        gphseq = self._colour_theme_dict["roles"]["graph_sequence"]
        self._colours_graphs = list(self._colours_df.loc[gphseq].hex)

        # traffic light graph colours
        tlight = self._colour_theme_dict["roles"]["trafficlight"]
        self._colours_trafficlight_rgb = {}
        self._colours_trafficlight_hex = {}
        for light, colour in tlight.items():
            self._colours_trafficlight_rgb[
                light.upper()
            ] = f"rgb({self._colours_df.loc[colour].rgb})"
            self._colours_trafficlight_hex[light.upper()] = self._colours_df.loc[
                colour
            ].hex

        # set up element colours
        self._colours_elements = {
            "box_background": self._colours_df.loc[
                self._colour_theme_dict["roles"]["box_background"]
            ].hex,
            "axis": self._colours_df.loc[self._colour_theme_dict["roles"]["axis"]].hex,
            "spikes": self._colours_df.loc[
                self._colour_theme_dict["roles"]["spikes"]
            ].hex,
            "grid_line": self._colours_df.loc[
                self._colour_theme_dict["roles"]["grid_line"]
            ].hex,
            "primary_text": self._colours_df.loc[
                self._colour_theme_dict["roles"]["primary_text"]
            ].hex,
        }

    def _set_design_theme_adjustments(self, design_theme):
        """
        Define the formatting/design adjustments for the theme
        These will replace/overwrite those of any base pio theme selected
        """
        # make sure legal colour theme
        if design_theme is None:
            design_theme = DEFAULT_DESIGN_THEME
        design_theme = design_theme.lower()

        if design_theme not in self.available_design_theme_adjustments:
            msg = (
                "Invalid design theme provided. Cannot set make the design adjustments."
            )
            raise ValueError(msg)

        # record the design theme name
        self._design_theme_name = design_theme
        self._design_theme_dict = json.loads(self._design_theme_json[design_theme])

        # margins
        # self._plot_margins = self._design_theme_dict["plot"]["margins"]
        # self._streamlit_plot_margins =
        #       self._design_theme_dict["plot"]["margins_streamlit"]

        # table
        # self._table_formatting = self._design_theme_dict["table"]

        # specific formatting components

        # legend
        # if "legend_layout" in self._design_theme_dict:
        # self._legend_layout = go.Layout(
        #               legend =
        #                   self._design_theme_dict["legend_layout"])
        #    self._legend_layout = self._design_theme_dict["legend_layout"]
        # else:
        #    self._legend_layout = go.Layout()

        # graph format
        # if "graph_format" in self._design_theme_dict:
        #    self._graph_format = go.Layout(self._design_theme_dict["graph_format"])
        # else:
        #    self._graph_format = go.Layout()

    def activate_theme(
        self,
        base_theme=None,
        colour_theme=None,
        design_theme_adjustments=None,
    ):
        """
        Activate the theming for the plotly graphs

        Uses the currently set colour and design theme adjustments
        and legend layout and applies these to the base_theme (if
        base_theme=None, then uses the default base theme)
        """

        # make sure legal theme
        if base_theme is None:
            base_theme = DEFAULT_PIO_THEME
        base_theme = base_theme.lower()

        # set the various theme parts as selected (otherwise the
        # already loaded ones will be used)
        # Note - we skip "None" so that the user can easily
        # adjust one of the theme components
        if colour_theme is not None:
            self._set_colour_theme(colour_theme)
        if design_theme_adjustments is not None:
            self._set_design_theme_adjustments(design_theme_adjustments)

        # store the active base theme, colour and design theme adjustments in use
        # Note: they are not activated until they are run though
        # here - so they can be "_set_" but
        # they wont be used until they are activated with this function
        self.active_base_theme = base_theme
        self.active_colour_theme = self._colour_theme_name
        self.active_design_theme_adjustments = self._design_theme_name

        # store the parts of the theme the user/graphs will want to access directly
        self.pallette = self._colours_graphs
        self.trafficlight_rgb = self._colours_trafficlight_rgb
        self.trafficlight_hex = self._colours_trafficlight_hex
        # self.legend_layout = self._legend_layout
        # self.graph_format = self._graph_format

        # load the base theme from pio
        self._pio_template = pio.templates[base_theme]

        # make changes to the base theme
        self._format_theme()

        # create/overwrite the optimeering theme in pio & set it as the default
        pio.templates[OPTIMEERING_THEME] = self._pio_template
        pio.templates.default = OPTIMEERING_THEME

    # ______________________________________
    # General layout formatting
    # ______________________________________

    def _format_theme(self):
        this_theme = self._pio_template  # shorthand

        # set the structural (design) formatting
        # ======================================
        this_theme = this_theme.update(self._design_theme_dict)

        # set the colour theme formatting
        # ================================
        # plot background
        this_theme["layout"]["paper_bgcolor"] = self._colours_elements["box_background"]
        this_theme["layout"]["plot_bgcolor"] = self._colours_elements["box_background"]

        # axes. Here use the color property to set everything at once.
        # Maybe control finer later.
        this_theme["layout"]["xaxis"]["color"] = self._colours_elements["axis"]
        this_theme["layout"]["yaxis"]["color"] = self._colours_elements["axis"]
        this_theme["layout"]["xaxis"]["spikecolor"] = self._colours_elements["spikes"]
        this_theme["layout"]["xaxis"]["linecolor"] = self._colours_elements["axis"]
        this_theme["layout"]["yaxis"]["linecolor"] = self._colours_elements["axis"]
        this_theme["layout"]["yaxis"]["gridcolor"] = self._colours_elements["grid_line"]
        # graph series colours
        this_theme.layout.colorway = self._colours_graphs
