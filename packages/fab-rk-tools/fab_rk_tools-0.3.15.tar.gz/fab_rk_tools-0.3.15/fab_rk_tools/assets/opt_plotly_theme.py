import json

import pandas as pd
import plotly.io as pio

# ______________________________________
# Define themes
# ______________________________________
#

DEFAULT_COLOUR_THEME = "dark"
LIGHT_BASE_THEME = "plotly"
LIGHT_COLOUR_THEME = "light"
DEFAULT_DESIGN_THEME = "optidesign"
DEFAULT_BASE_THEME = "plotly_dark"  # base theme from pio to base everything on
OPTIMEERING_THEME = "optitheme"  # name to use in pio. Doesn't matter what it is.

# default theme definition

OLD_DEFAULT_COLOUR_THEME_JSON = """{
    "colors": [
        {"name":"blue_dark","hex":"#415B8C"},
        {"name":"blue_mid","hex":"#799BD9"},
        {"name":"blue_light","hex":"#BFCFED"},
        {"name":"lime_light","hex":"#B5D964"},
        {"name":"green_mid","hex":"#9CB36B"},
        {"name":"green_dark","hex":"#778C48"},
        {"name":"dusky_light","hex":"#D99A8F"},
        {"name":"dusky_mid","hex":"#C15B49"},
        {"name":"dusky_dark","hex":"#A74A39"},
        {"name":"yellow_mid","hex":"#F6DE50"},
        {"name":"blue_very_dark","hex":"#0D121C"},
        {"name":"off_white","hex":"#F7F8FA"},
        {"name": "grey_light", "hex": "#bcc4c8"},
        {"name": "grey_mid", "hex": "#788991"}

    ],
    "roles": {
        "box_background": "blue_very_dark",
        "primary_text": "off_white",
        "graph_sequence": ["blue_mid", "lime_light", "dusky_light", "green_dark",
            "blue_light", "dusky_mid", "blue_dark"],
        "axis": "grey_light",
        "grid_line": "grey_mid",
        "spikes": "grey_mid",
        "trafficlight": {
            "GREEN": "green_mid",
            "YELLOW": "yellow_mid",
            "RED": "dusky_dark",
            "default": "blue_mid"
        },
        "direction": {
            "UP": "
        }
    }

}"""

DEFAULT_COLOUR_THEME_JSON = """{
    "colors": [
        {"name":"turquoise_green","hex":"#99D6AE"},
        {"name":"magic_mint","hex":"#B5F7CA"},
        {"name":"light_salmon","hex":"#FF9B70"},
        {"name":"salmon_pink","hex":"#F59A9F"},
        {"name":"light_sky_blue","hex":"#8BD2F9"},
        {"name":"dark_sky_blue","hex":"#6DA5C5"},
        {"name":"medium_carmine","hex":"#A74A39"},
        {"name":"minion_yellow","hex":"#F7E164"},
        {"name":"rich_black","hex":"#0D121C"},
        {"name":"off_white","hex":"#F7F8FA"},
        {"name": "grey_light", "hex": "#bcc4c8"},
        {"name": "grey_mid", "hex": "#788991"}
    ],
    "roles": {
        "box_background": "rich_black",
        "primary_text": "off_white",
        "graph_sequence": ["light_sky_blue", "light_salmon", "magic_mint",
            "minion_yellow", "turquoise_green", "dark_sky_blue", "medium_carmine"],
        "axis": "grey_light",
        "grid_line": "grey_mid",
        "spikes": "grey_mid",
        "trafficlight": {
            "GREEN": "turquoise_green",
            "YELLOW": "minion_yellow",
            "RED": "medium_carmine",
            "default": "minion_yellow"
        },
        "direction": {
            "up": "light_sky_blue",
            "down": "light_salmon",
            "neutral": "turquoise_green"
        }
    }

}"""

LIGHT_COLOUR_THEME_JSON = """{
    "colors": [
        {"name":"turquoise_green","hex":"#99D6AE"},
        {"name":"magic_mint","hex":"#B5F7CA"},
        {"name":"light_salmon","hex":"#FF9B70"},
        {"name":"salmon_pink","hex":"#F59A9F"},
        {"name":"light_sky_blue","hex":"#8BD2F9"},
        {"name":"dark_sky_blue","hex":"#6DA5C5"},
        {"name":"medium_carmine","hex":"#A74A39"},
        {"name":"minion_yellow","hex":"#F7E164"},
        {"name":"rich_black","hex":"#0D121C"},
        {"name":"off_white","hex":"#F7F8FA"},
        {"name": "grey_light", "hex": "#bcc4c8"},
        {"name": "grey_mid", "hex": "#788991"},
        {"name": "black_coral", "hex": "#535F65"}
    ],
    "roles": {
        "box_background": "off_white",
        "primary_text": "rich_black",
        "graph_sequence": ["light_sky_blue", "salmon_pink", "dark_sky_blue",
            "turquoise_green", "medium_carmine"],
        "axis": "black_coral",
        "grid_line": "grey_mid",
        "spikes": "grey_mid",
        "trafficlight": {
            "GREEN": "turquoise_green",
            "YELLOW": "minion_yellow",
            "RED": "medium_carmine",
            "default": "minion_yellow"
        },
        "direction": {
            "up": "dark_sky_blue",
            "down": "salmon_pink",
            "neutral": "turquoise_green"
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
    Class that implements the plotly themeing via json strings

    Separates colour and "design" formatting - so you can keep the same design and change colours easily for example

    As the plotly.io.templates are globally defined, we also so a (sort of) global definition for FabPlotlyTheme - that is,
    there is at most one instance of FabPlotlyTheme possible.

    So, a theme is instantiated via:

        my_theme = FabPlotlyTheme()

    This will create a theme object with the default theme loaded if one does not exist. This also includes defining the default theme in
    plotly.io.templates. If a FabPlotlyTheme object exists, then my_theme will just point to it.

    This way you can keep a consistent formatting over all graphs in the same "container"

    You can load in new colour themes and design themes via the load_colour_theme() and load_design_theme_adjustments() methods.

    A complete active theme can be set via the activate_theme() method.

    By defining e.g. new colours in a json string, loading them, and activating theme like this:

        my_theme.load_colour_theme(colour_theme="MyNewColours", colour_theme_json=A_JSON_STRING)
        my_theme.activate_theme(colour_theme="MyNewColours")

    you switch colours whilst keeping all other formatting for the graphs. New graphs will be displayed with the new colours.

    You get access to the default (active) plotly.io.template via the pio_default_template() method.

    This structure enables us to define objects outside of the plotly.io.template structure. One example of this is the trafficlight
    colours for traffic light diagrams/graphs. As a traffic light graph does not exist in plotly, we need to make one using other
    plotly graph methods. But, this makes it hard to set colours without overwriting the colours in other graphs using these
    objects. Instead, these are stored in my_theme.trafficlight_hex property, and can be accessed by
    our trafficlight graphing code. The trafficlight colours are defined in the colour json (either the default, or one loaded).

    """

    def __init__(self):
        # actives are none at start
        self.active_base_theme = None
        self.active_colour_theme = None
        self.active_design_theme_adjustments = None

        # load the inbuilt colour and design adjustment themes
        self._colour_theme_json = dict()
        self._design_theme_json = dict()
        # available stuff
        self.available_colour_themes = list()
        self.available_design_theme_adjustments = list()
        # load the defaults so we have at least these
        self.load_colour_theme(
            colour_theme=DEFAULT_COLOUR_THEME,
            colour_theme_json=DEFAULT_COLOUR_THEME_JSON,
        )
        self.load_colour_theme(
            colour_theme=LIGHT_COLOUR_THEME,
            colour_theme_json=LIGHT_COLOUR_THEME_JSON,
        )
        self.load_design_theme_adjustments(
            design_theme=DEFAULT_DESIGN_THEME,
            design_theme_json=DEFAULT_DESIGN_THEME_JSON,
        )

        # set the default themes to active
        self._set_colour_theme(colour_theme=DEFAULT_COLOUR_THEME)
        self._set_design_theme_adjustments(design_theme=DEFAULT_DESIGN_THEME)

        # initialize instance variables
        self.pallette = None
        self.trafficlight_hex = None
        self.direction_hex = None
        self.monochrome_hex = None
        self.fan_hex = None
        self._pio_template = None

        # activate the theme, using the defaults (these have just been set)
        self.activate_theme()

    def load_colour_theme(self, colour_theme, colour_theme_json):
        """
        Load in a new colour theme

        colour_theme: str, name of the new theme
        colour_theme_json: json, json definition of the theme colours.

        """

        # at some stage we should error check the json
        self._colour_theme_json[colour_theme] = colour_theme_json
        # available stuff
        self.available_colour_themes.append(colour_theme)

    def load_design_theme_adjustments(self, design_theme, design_theme_json):
        self._design_theme_json[design_theme] = design_theme_json
        # available stuff
        self.available_design_theme_adjustments.append(design_theme)

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

        # copy colors to colours and colours to colors...
        if "colours" in self._colour_theme_dict:
            # colours overwrites if both are provided
            self._colour_theme_dict["colors"] = self._colour_theme_dict[
                "colours"
            ].copy()
        elif "colors" in self._colour_theme_dict:
            self._colour_theme_dict["colours"] = self._colour_theme_dict[
                "colors"
            ].copy()
        else:
            msg = "No colours/colors provided in colour theme - please define"
            raise ValueError(msg)

        # store colours in a dataframe
        self._colours_df = pd.DataFrame(self._colour_theme_dict["colors"])
        self._colours_df = self._colours_df.set_index("name")

        # set up a list with graph colours in order
        gphseq = self._colour_theme_dict["roles"]["graph_sequence"]
        self._colours_graphs = list(self._colours_df.loc[gphseq].hex)

        # traffic light graph colours
        tl = self._colour_theme_dict["roles"]["trafficlight"]
        # self._colours_trafficlight_rgb=dict()
        self._colours_trafficlight_hex = dict()
        for light, colour in tl.items():
            # self._colours_trafficlight_rgb[light.upper()]=f"rgb({self._colours_df.loc[colour].rgb})"
            self._colours_trafficlight_hex[light.upper()] = self._colours_df.loc[
                colour
            ].hex

        # monochrome
        if "monochrome" in self._colour_theme_dict["roles"]:
            colour = self._colour_theme_dict["roles"]["monochrome"]
        else:
            colour = self._colour_theme_dict["colors"][0]["name"]
        self._colours_monochrome_hex = self._colours_df.loc[colour].hex

        # fan colour
        if "fan" in self._colour_theme_dict["roles"]:
            colour = self._colour_theme_dict["roles"]["fan"]
            self._colours_fan_hex = self._colours_df.loc[colour].hex
        else:
            self._colours_fan_hex = self._colours_graphs[0]  # already stored as hex

        # direction graph colours
        dr = self._colour_theme_dict["roles"]["direction"]
        # self._colours_trafficlight_rgb=dict()
        self._colours_direction_hex = dict()
        for direction, colour in dr.items():
            # self._colours_trafficlight_rgb[light.upper()]=f"rgb({self._colours_df.loc[colour].rgb})"
            self._colours_direction_hex[direction] = self._colours_df.loc[colour].hex

        # set up element colours
        self._colours_elements = dict(
            box_background=self._colours_df.loc[
                self._colour_theme_dict["roles"]["box_background"]
            ].hex,
            axis=self._colours_df.loc[self._colour_theme_dict["roles"]["axis"]].hex,
            spikes=self._colours_df.loc[self._colour_theme_dict["roles"]["spikes"]].hex,
            grid_line=self._colours_df.loc[
                self._colour_theme_dict["roles"]["grid_line"]
            ].hex,
            primary_text=self._colours_df.loc[
                self._colour_theme_dict["roles"]["primary_text"]
            ].hex,
        )

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

    def activate_theme(
        self, base_theme=None, colour_theme=None, design_theme_adjustments=None
    ):
        """
        Activate the theming for the plotly graphs

        Uses the currently set colour and design theme adjustments and legend layout and applies these
        to the base_theme (if base_theme=None, then uses the default base theme)
        """

        # make sure legal theme
        if base_theme is None:
            base_theme = DEFAULT_BASE_THEME
        base_theme = base_theme.lower()

        # set the various theme parts as selected (otherwise the already loaded ones will be used)
        # Note - we skip "None" so that the user can easily adjust one of the theme components
        if colour_theme is not None:
            self._set_colour_theme(colour_theme)
        if design_theme_adjustments is not None:
            self._set_design_theme_adjustments(design_theme_adjustments)

        # store the active base theme, colour and design theme adjustments in use
        # Note: they are not activated until they are run though here - so they can be "_set_" but
        # they won't be used until they are activated with this function
        self.active_base_theme = base_theme
        self.active_colour_theme = self._colour_theme_name
        self.active_design_theme_adjustments = self._design_theme_name

        # store the parts of the theme the user/graphs will want to access directly
        self.pallette = self._colours_graphs
        # self.trafficlight_rgb=self._colours_trafficlight_rgb
        self.trafficlight_hex = self._colours_trafficlight_hex
        self.direction_hex = self._colours_direction_hex
        self.monochrome_hex = self._colours_monochrome_hex
        self.fan_hex = self._colours_fan_hex

        # load the base theme from pio
        self._pio_template = pio.templates[base_theme]

        # make changes to the base theme
        this_theme = self._pio_template  # shorthand

        # set the structural (design) formatting
        # ======================================
        this_theme = this_theme.update(self._design_theme_dict)

        # set the colour theme formatting
        # ================================
        # plot background
        this_theme["layout"]["paper_bgcolor"] = self._colours_elements["box_background"]
        this_theme["layout"]["plot_bgcolor"] = self._colours_elements["box_background"]

        # title
        this_theme["layout"]["title"]["font"]["color"] = self._colours_elements[
            "primary_text"
        ]

        # axes. Here use the color property to set everything at once. Maybe control finer later.
        this_theme["layout"]["xaxis"]["color"] = self._colours_elements["axis"]
        this_theme["layout"]["yaxis"]["color"] = self._colours_elements["axis"]
        this_theme["layout"]["xaxis"]["spikecolor"] = self._colours_elements["spikes"]
        this_theme["layout"]["xaxis"]["linecolor"] = self._colours_elements["axis"]
        this_theme["layout"]["yaxis"]["linecolor"] = self._colours_elements["axis"]
        this_theme["layout"]["yaxis"]["gridcolor"] = self._colours_elements["grid_line"]
        this_theme["layout"]["yaxis"]["tickfont"]["color"] = self._colours_elements[
            "primary_text"
        ]
        this_theme["layout"]["xaxis"]["tickfont"]["color"] = self._colours_elements[
            "primary_text"
        ]
        this_theme["layout"]["yaxis"]["title"]["font"][
            "color"
        ] = self._colours_elements["primary_text"]
        this_theme["layout"]["xaxis"]["title"]["font"][
            "color"
        ] = self._colours_elements["primary_text"]
        # graph series colours
        this_theme.layout.colorway = self._colours_graphs

        # create/overwrite the optimeering theme in pio & set it as the default
        pio.templates[OPTIMEERING_THEME] = self._pio_template
        pio.templates.default = OPTIMEERING_THEME

    def pio_default_template(self):
        return pio.templates[pio.templates.default]

    def hex_to_rgb(self, hex):
        """
        Convert list or dict of hex colour codes to list or dict of rgb
        """
        if isinstance(hex, str):
            hex = [hex]
        if not (isinstance(hex, list) or isinstance(hex, dict)):
            msg = "List or dict of hex codes expected"
            raise ValueError(msg)

        # use a dict to process
        if isinstance(hex, list):
            hexdict = dict()
            for h in hex:
                hexdict[h] = h
        else:
            hexdict = hex.copy()

        rgbres = dict()
        for key, col in hexdict.items():
            h = col.lstrip("#")
            rgb = list(int(h[i : i + 2], 16) for i in (0, 2, 4))
            rgb = "rgb" + str(tuple(rgb))
            rgbres[key] = rgb

        if isinstance(hex, list):
            return list(rgbres.values())
        else:
            return rgbres
