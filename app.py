from flask import Flask
import ghhops_server as hs
import pandas as pd
import os

import all_graphs
from utils import *


# register hops app as middleware
app = Flask(__name__)
hops: hs.HopsFlask = hs.Hops(app)

@app.route('/')
def index():
    return 'Hello World!'

@hops.component(
    "/dt_to_df",
    name="datatree to dataframe",
    nickname="dtdf",
    description="Converts any str,int,float datatree to a csv representation of a dataframe",
    inputs=[
        hs.HopsString("Data as tree", "Dt", "Data tree to convert", hs.HopsParamAccess.TREE),
        hs.HopsString("Tree structure labels", "L", "List of the path labels (what the tree structure represent)",
                      hs.HopsParamAccess.LIST),
        hs.HopsString("Datatype", "D", "What does the data represent? Number of elements should match the number of"
                                       "elements in each branches of the datatree", hs.HopsParamAccess.LIST),
    ],
    outputs=[
        hs.HopsString("DfCSV", "Df", "Dataframe as a csv."
                                     "\nNote that you might not be able to use panel on this output."),
    ]
)
def better(data_tree: dict, path_labels: list, data_type: list):

    if len(list(data_tree.keys())[0]) != len(data_type):
        # THROW A WARNING !!
        # Hops limitation. If needed, just print stuff, and keep checking terminal window
        pass

    clean_tree = clean_dict_datatype(data_tree)
    renamed_key = temp_rename_dict(clean_tree)
    temp_list = list_key_path(renamed_key)
    partitioned = sub_lister(temp_list, len(path_labels))

    transposed = list(map(lambda *a: list(a), *partitioned))

    path_dict = label_dict(transposed, path_labels)
    dict_list = dicts_for_datatypes(data_tree, data_type)
    final_dict = dict_merger(path_dict, dict_list)
    the_dataframe = pd.DataFrame.from_dict(final_dict)

    # format incompatibility fix
    the_actual_dataframe = fix_one_item_list(the_dataframe, data_type)

    return the_actual_dataframe.to_csv(index=False, line_terminator='@')


@hops.component(
    "/presets",
    name="Available presets",
    nickname="AvPre",
    description="Returns available plots and palettes for selected types",
    inputs=[
        hs.HopsString("Plot types", "Plots", "Select a plot type to see all the supported plots for that type"
                                             "\nChoose from: 'relational', 'distribution', 'categorical'"),
        hs.HopsString("Palette types", "Palettes", "Select a palette type to see all the supported palettes for that "
                                                   "type"
                                                   "\nChoose from: 'default', 'diverging', 'qualitative', 'sequential'")
    ],
    outputs=[
        hs.HopsString("Available plots", "Plots", "Currently available plots", hs.HopsParamAccess.LIST),
        hs.HopsString("Available palettes", "Palettes", "Currently available palettes", hs.HopsParamAccess.LIST)
    ]
)
def available_presets(plot_type='categorical', palette_type='default'):
    supported_plots = {
        'relational': ['lineplot', 'relplot', 'scatterplot'],
        'distribution': ['displot', 'histplot', 'kdeplot'],
        'categorical': ['catplot', 'stripplot', 'swarmplot', 'boxplot', 'violinplot', 'boxenplot', 'pointplot',
                        'barplot', 'countplot']
    }

    supported_palettes = {
        'default': ['deep', 'muted', 'pastel', 'bright', 'dark', 'colorblind'],
        'diverging': ['BrBG', 'PRGn', 'PiYG', 'PuOr', 'RdBu', 'RdGy', 'RdYlBu', 'RdYlBu', 'Spectral'],
        'qualitative': ['Accent', 'Dark2', 'Paired', 'Pastel1', 'Pastel2', 'Set1', 'Set2', 'Set3'],
        'sequential': ['Blues', 'BuGn', 'BuPu', 'GnBu', 'Greens', 'Greys', 'OrRd', 'Oranges', 'PuBu', 'PuBuGn', 'PuRd',
                       'Purples', 'RdPu', 'Reds', 'YlGn', 'YlGnBu', 'YlOrBr', 'YlOrRd']
    }

    return supported_plots[plot_type], supported_palettes[palette_type]


# ---------------------------------
# CURRENTLY AVAILABLE PLOTS

# NO DEFAULT EXAMPLE, WHICH SHOULD PRODUCE A RELPLOT (See one function after this one)
@hops.component(
    "/no_default",
    name="dataframes relploter",
    nickname="relDF",
    description="Relplot a dataframe",
    inputs=[
        hs.HopsString("Dataframe", "Df", "Dataframe to relplot"),
        hs.HopsString("X axis", "X", "What's your X value?"),
        hs.HopsString("Y axis", "Y", "What's your Y value? Has to refer to numerical values"),
        hs.HopsString("Hue", "h", "Column value to differentiate X and Y with", default=None),
        hs.HopsString("Palette", "p", "Seaborn palette for your graph."
                                      "\nInput a valid name or select one from the output of the 'preset' component"
                                      "\nDefault = 'deep'"),
        hs.HopsBoolean("Plot", "P", "Plot me!")
    ],
    outputs=[
        hs.HopsString("Base64 png", "img_str", "Image as base64 bitmap."),
    ]
)
def rel_df(csv_df1: str, x_ax, y_ax, g_hue, g_palette="deep", plot=False):
    # load csv to df
    the_dataframe = csv_to_df(csv_df1)
    if plot:
        return all_graphs.no_default(the_dataframe, x_ax, y_ax, g_hue, g_palette)


# ---------------------------------
# RELATIONAL PLOTS


@hops.component(
    "/relplot",
    name="dataframes relploter",
    nickname="relDF",
    description="Relplot a dataframe",
    inputs=[
        hs.HopsString("Dataframe", "Df", "Dataframe to relplot"),
        hs.HopsString("X axis", "X", "What's your X value?"),
        hs.HopsString("Y axis", "Y", "What's your Y value? Has to refer to numerical values"),
        hs.HopsString("Hue", "h", "Column value to differentiate X and Y with"),
        hs.HopsString("Palette", "p", "Seaborn palette for your graph."
                                      "\nInput a valid name or select one from the output of the 'preset' component"
                                      "\nDefault = 'deep'"),
        hs.HopsBoolean("Plot", "P", "Plot me!")
    ],
    outputs=[
        hs.HopsString("Base64 png", "img_str", "Image as base64 bitmap."),
    ]
)
def rel_df(csv_df1: str, x_ax, y_ax, g_hue='', g_palette="deep", plot: bool = False):
    # load csv to df
    the_dataframe = csv_to_df(csv_df1)
    if plot:
        return all_graphs.rel(the_dataframe, x_ax, y_ax, g_hue, g_palette)


@hops.component(
    "/scatterplot",
    name="dataframes scatterploter",
    nickname="scatterDF",
    description="Scatterplot a dataframe",
    inputs=[
        hs.HopsString("Dataframe", "Df", "Dataframe to scatterplot"),
        hs.HopsString("X axis", "X", "What's your X value?"),
        hs.HopsString("Y axis", "Y", "What's your Y value? Has to refer to numerical values"),
        hs.HopsString("Hue", "h", "Column value to differentiate X and Y with"),
        hs.HopsString("Palette", "p", "Seaborn palette for your graph."
                                      "\nInput a valid name or select one from the output of the 'preset' component"
                                      "\nDefault = 'deep'"),
        hs.HopsBoolean("Plot", "P", "Plot me!")
    ],
    outputs=[
        hs.HopsString("Base64 png", "img_str", "Image as base64 bitmap."),
    ]
)
def scatter_df(csv_df1: str, x_ax, y_ax, g_hue='', g_palette="deep", plot: bool = False):
    # load csv to df
    the_dataframe = csv_to_df(csv_df1)
    if plot:
        return all_graphs.scatter(the_dataframe, x_ax, y_ax, g_hue, g_palette)


@hops.component(
    "/lineplot",
    name="dataframes lineploter",
    nickname="lineDF",
    description="Lineplot a dataframe",
    inputs=[
        hs.HopsString("Dataframe", "Df", "Dataframe to lineplot"),
        hs.HopsString("X axis", "X", "What's your X value?"),
        hs.HopsString("Y axis", "Y", "What's your Y value? Has to refer to numerical values"),
        hs.HopsString("Hue", "h", "Column value to differentiate X and Y with"),
        hs.HopsString("Palette", "p", "Seaborn palette for your graph."
                                      "\nInput a valid name or select one from the output of the 'preset' component"
                                      "\nDefault = 'deep'"),
        hs.HopsBoolean("Plot", "P", "Plot me!")
    ],
    outputs=[
        hs.HopsString("Base64 png", "img_str", "Image as base64 bitmap."),
    ]
)
def line_df(csv_df1: str, x_ax, y_ax, g_hue='', g_palette="deep", plot: bool = False):
    # load csv to df
    the_dataframe = csv_to_df(csv_df1)
    if plot:
        return all_graphs.line(the_dataframe, x_ax, y_ax, g_hue, g_palette)


# -------------------------------------------------
# DISTRIBUTION PLOTS


@hops.component(
    "/displot",
    name="dataframes disploter",
    nickname="disDF",
    description="Displot a dataframe in one dimension",
    inputs=[
        hs.HopsString("Dataframe", "Df", "Dataframe to displot"),
        hs.HopsString("X axis", "X", "What's your X value?"),
        hs.HopsString("Y axis", "Y", "What's your Y value?"),
        hs.HopsString("Hue", "h", "Column value to differentiate X and Y with"),
        hs.HopsString("Kind", "k", "Selects the underlying plotting function and determines the additional set of "
                                   "valid parameters.\nChoose from 'hist', 'kde' or 'ecdf' \nDefault: 'hist'"),
        hs.HopsBoolean("Rug", "r", "If True, show each observation with marginal ticks"),
        hs.HopsBoolean("Legend", "l", "If False, suppress the legend for semantic variables"),
        hs.HopsString("Palette", "p", "Seaborn palette for your graph."
                                      "\nInput a valid name or select one from the output of the 'preset' component"
                                      "\nDefault = 'deep'"),
        hs.HopsBoolean("Plot", "P", "Plot me!")
    ],
    outputs=[
        hs.HopsString("Base64 png", "img_str", "Image as base64 bitmap."),
    ]
)
def dis_df(csv_df1: str, x_ax, y_ax='', g_hue='', g_kind='hist', g_rug=False, g_legend=True, g_palette="deep",
           plot: bool = False):
    # load csv to df
    the_dataframe = csv_to_df(csv_df1)
    if plot:
        return all_graphs.dis(the_dataframe, x_ax, y_ax, g_hue, g_kind, g_rug, g_legend, g_palette)


@hops.component(
    "/histplot",
    name="dataframes histploter",
    nickname="histDF_1",
    description="Histplot a dataframe",
    inputs=[
        hs.HopsString("Dataframe", "Df", "Dataframe to histplot"),
        hs.HopsString("X axis", "X", "What's your X value?"),
        hs.HopsString("Y axis", "y", "What's your Y value? (optional)"),
        hs.HopsString("Hue", "h", "Column value to differentiate X and Y with"),
        hs.HopsString("Stat", "s", "Aggregate statistic to compute in each bin"
                                   "\nChoose from 'count', 'frequency', 'probability', 'percent' or 'density'"
                                   "\nDefault: 'count'"),
        hs.HopsBoolean("Cumulative", "c", "If True, plot the cumulative counts as bins increase."),
        hs.HopsString("Multiple", "m", "Approach to resolving multiple elements when semantic mapping creates subsets. "
                                       "Only relevant with univariate data"
                                       "\nChoose from 'layer', 'dodge', 'stack', 'fill' \nDefault: 'layer'"),
        hs.HopsString("Element", "e", "Visual representation of the histogram statistic. Only relevant with univariate "
                                      "data \nChoose from 'bars', 'step' or 'poly' \nDefault: 'bars'"),
        hs.HopsBoolean("Fill", "f", "If True, fill in the space under the histogram. Only relevant with "
                                    "univariate data."),
        hs.HopsNumber("Shrink", "s", "Scale the width of each bar relative to the binwidth by this factor."
                                     "Only relevant with univariate data"),
        hs.HopsBoolean("KDE", "k", "If True, compute a kernel density estimate to smooth the distribution and show on "
                                   "the plot as (one or more) line(s). Only relevant with univariate data."),
        hs.HopsBoolean("Legend", "l", "If False, suppress the legend for semantic variables"),
        hs.HopsString("Palette", "p", "Seaborn palette for your graph."
                                      "\nInput a valid name or select one from the output of the 'preset' component"
                                      "\nDefault = 'deep'"),
        hs.HopsBoolean("Plot", "P", "Plot me!")
    ],
    outputs=[
        hs.HopsString("Base64 png", "img_str", "Image as base64 bitmap."),
    ]
)
def hist_df(csv_df1: str, x_ax, y_ax='', g_hue='', g_stat='count', g_cumulative=False, g_multiple='layer',
            g_element='bars', g_fill=True, g_shrink=1, g_kde=False, g_legend=True, g_palette="deep",
            plot: bool = False):
    # load csv to df
    the_dataframe = csv_to_df(csv_df1)
    if plot:
        return all_graphs.hist(the_dataframe, x_ax, y_ax, g_hue, g_stat, g_cumulative, g_multiple, g_element, g_fill, g_shrink,
                        g_kde, g_legend, g_palette)


@hops.component(
    "/kdeplot",
    name="dataframes kdeploter",
    nickname="kdeDF",
    description="Kdeplot a dataframe",
    inputs=[
        hs.HopsString("Dataframe", "Df", "Dataframe to kdeplot"),
        hs.HopsString("X axis", "X", "What's your X value? Has to be numerical"),
        hs.HopsString("Y axis", "y", "What's your Y value? Has to be numerical (but is optional)"),
        hs.HopsString("Hue", "h", "Column value to differentiate X and Y with"),
        hs.HopsNumber("Cut", "c", "Factor, multiplied by the smoothing bandwidth, that determines how far the "
                                  "evaluation grid extends past the extreme datapoints. "
                                  "\nWhen set to 0, truncate the curve at the data limits."),
        hs.HopsBoolean("Cumulative", "c", "If True, estimate a cumulative distribution function"),
        hs.HopsString("Multiple", "m", "Approach to resolving multiple elements when semantic mapping creates subsets. "
                                       "Only relevant with univariate data"
                                       "\nChoose from 'layer', 'stack', 'fill' \nDefault: 'layer'"),
        hs.HopsBoolean("Common norm", "cn", "If True, scale each conditional density by the number of observations such"
                                            "that the total area under all densities sums to 1. "
                                            "\nOtherwise, normalize each density independently."),
        hs.HopsBoolean("Common grid", "cg", "If True, use the same evaluation grid for each kernel density estimate. "
                                            "\nOnly relevant with univariate data."),
        hs.HopsInteger("Levels", "l", "Number of contour levels or values to draw contours at."
                                      "\nLevels correspond to iso-proportions of the density: e.g., 20% of the "
                                      "probability mass will lie below the contour drawn for 0.2. Only relevant with "
                                      "bivariate data."),
        hs.HopsNumber("Thresh", "t", "Lowest iso-proportion level at which to draw a contour line. Ignored when levels "
                                     "is a vector. Only relevant with bivariate data."),
        hs.HopsNumber("Alpha", "a", "Alpha value for the fill option"),
        hs.HopsBoolean("Fill", "f", "Fill ?"),
        hs.HopsBoolean("Legend", "l", "If False, suppress the legend for semantic variables"),
        hs.HopsString("Palette", "p", "Seaborn palette for your graph."
                                      "\nInput a valid name or select one from the output of the 'preset' component"
                                      "\nDefault = 'deep'"),
        hs.HopsBoolean("Plot", "P", "Plot me!")
    ],
    outputs=[
        hs.HopsString("Base64 png", "img_str", "Image as base64 bitmap."),
    ]
)
def kde_df(csv_df1: str, x_ax, y_ax='', g_hue='', g_cut=3, g_cumulative=False, g_multiple='layer', g_common_norm=True,
           g_common_grid=False, g_levels=10, g_thresh=0.05, g_alpha=1, g_fill=False, g_legend=True,
           g_palette="deep", plot: bool = False):
    # load csv to df
    the_dataframe = csv_to_df(csv_df1)
    if plot:
        return all_graphs.kde(the_dataframe, x_ax, y_ax, g_hue, g_cut, g_cumulative, g_multiple, g_common_norm, g_common_grid,
                       g_levels, g_thresh, g_alpha, g_fill, g_legend, g_palette)


# -------------------------------------------------
# CATEGORICAL PLOTS


@hops.component(
    "/catplot",
    name="dataframes catploter",
    nickname="catDF",
    description="Catplot a dataframe",
    inputs=[
        hs.HopsString("Dataframe", "Df", "Dataframe to catplot"),
        hs.HopsString("X axis", "X", "What's your X value?"),
        hs.HopsString("Y axis", "Y", "What's your Y value? Has to refer to numerical values"),
        hs.HopsString("Hue", "h", "Column value to differentiate X and Y with"),
        hs.HopsString("ci", "c", "Confidence interval can be set to 'sd' as for 'standard deviation'"),
        hs.HopsInteger("Seed", "s", "Seed for reproducible bootstrapping"),
        hs.HopsString("Kind", "k", "The kind of plot to draw, corresponds to the name of a categorical axes-level "
                                   "plotting function"
                                   "\nChoose from: 'strip', 'swarm', 'box', 'violin', 'boxen', 'point', 'bar', "
                                   "or 'count'"
                                   "\nDefault = 'strip'"),
        hs.HopsString("Palette", "p", "Seaborn palette for your graph."
                                      "\nInput a valid name or select one from the output of the 'preset' component"
                                      "\nDefault = 'deep'"),
        hs.HopsBoolean("Plot", "P", "Plot me!")
    ],
    outputs=[
        hs.HopsString("Base64 png", "img_str", "Image as base64 bitmap."),
    ]
)
def cat_df(csv_df1: str, x_ax, y_ax, g_hue='', g_ci="None", g_seed=2, g_kind="strip", g_palette="deep",
           plot: bool = False):
    # load csv to df
    the_dataframe = csv_to_df(csv_df1)
    if plot:
        return all_graphs.cat(the_dataframe, x_ax, y_ax, g_hue, g_ci, g_seed, g_kind, g_palette)


@hops.component(
    "/stripplot",
    name="dataframes stripploter",
    nickname="stripDF",
    description="Stripplot a dataframe",
    inputs=[
        hs.HopsString("Dataframe", "Df", "Dataframe to stripplot"),
        hs.HopsString("X axis", "X", "What's your X value?"),
        hs.HopsString("Y axis", "Y", "What's your Y value? Has to refer to numerical values"),
        hs.HopsString("Hue", "h", "Column value to differentiate X and Y with"),
        hs.HopsNumber("Jitter", "j", "Amount of jitter (only along the categorical axis) to apply"),
        hs.HopsString("Palette", "p", "Seaborn palette for your graph."
                                      "\nInput a valid name or select one from the output of the 'preset' component"
                                      "\nDefault = 'deep'"),
        hs.HopsNumber("Size", "s", "Radius of the markers, in points"),
        hs.HopsBoolean("Plot", "P", "Plot me!")
    ],
    outputs=[
        hs.HopsString("Base64 png", "img_str", "Image as base64 bitmap."),
    ]
)
def strip_df(csv_df1: str, x_ax, y_ax, g_hue='', g_jitter=True, g_palette="deep", g_size=2, plot: bool = False):
    # load csv to df
    the_dataframe = csv_to_df(csv_df1)
    if plot:
        return all_graphs.strip(the_dataframe, x_ax, y_ax, g_hue, g_jitter, g_palette, g_size)


@hops.component(
    "/swarmplot",
    name="dataframes swarmploter",
    nickname="swarmDF",
    description="Swarmplot a dataframe",
    inputs=[
        hs.HopsString("Dataframe", "Df", "Dataframe to swarmplot"),
        hs.HopsString("X axis", "X", "What's your X value?"),
        hs.HopsString("Y axis", "Y", "What's your Y value? Has to refer to numerical values"),
        hs.HopsString("Hue", "h", "Column value to differentiate X and Y with"),
        hs.HopsBoolean("Dodge", "d", "Setting this to True will separate the strips for different hue levels along "
                                     "the categorical axis"),
        hs.HopsString("Palette", "p", "Seaborn palette for your graph."
                                      "\nInput a valid name or select one from the output of the 'preset' component"
                                      "\nDefault = 'deep'"),
        hs.HopsNumber("Size", "s", "Radius of the markers, in points"),
        hs.HopsBoolean("Plot", "P", "Plot me!")
    ],
    outputs=[
        hs.HopsString("Base64 png", "img_str", "Image as base64 bitmap."),
    ]
)
def swarm_df(csv_df1: str, x_ax, y_ax, g_hue='', g_dodge=False, g_palette="deep", g_size=2, plot: bool = False):
    # load csv to df
    the_dataframe = csv_to_df(csv_df1)
    if plot:
        return all_graphs.swarm(the_dataframe, x_ax, y_ax, g_hue, g_dodge, g_palette, g_size)


@hops.component(
    "/boxplot",
    name="dataframes boxploter",
    nickname="boxDF",
    description="Boxplot a dataframe",
    inputs=[
        hs.HopsString("Dataframe", "Df", "Dataframe to boxplot"),
        hs.HopsString("X axis", "X", "What's your X value?"),
        hs.HopsString("Y axis", "Y", "What's your Y value? Has to refer to numerical values"),
        hs.HopsString("Hue", "h", "Column value to differentiate X and Y with"),
        hs.HopsString("Palette", "p", "Seaborn palette for your graph."
                                      "\nInput a valid name or select one from the output of the 'preset' component"
                                      "\nDefault = 'deep'"),
        hs.HopsBoolean("Plot", "P", "Plot me!")
    ],
    outputs=[
        hs.HopsString("Base64 png", "img_str", "Image as base64 bitmap."),
    ]
)
def box_df(csv_df1: str, x_ax, y_ax, g_hue='', g_palette="deep", plot: bool = False):
    # load csv to df
    the_dataframe = csv_to_df(csv_df1)
    if plot:
        img = all_graphs.box(the_dataframe, x_ax, y_ax, g_hue, g_palette)
        return img


@hops.component(
    "/violinplot",
    name="dataframes violinploter",
    nickname="violinDF",
    description="Violinplot a dataframe",
    inputs=[
        hs.HopsString("Dataframe", "Df", "Dataframe to violinplot"),
        hs.HopsString("X axis", "X", "What's your X value?"),
        hs.HopsString("Y axis", "Y", "What's your Y value? Has to refer to numerical values"),
        hs.HopsString("Hue", "h", "Column value to differentiate X and Y with"),
        hs.HopsNumber("bw", "b", "The scale factor to use when computing the kernel bandwidth"),
        hs.HopsString("Inner", "i", "Representation of the datapoints in the violin interior"
                                    "\nChoose from 'box', 'quartile', 'point', or 'stick'"
                                    "\nDefault = 'box'"),
        hs.HopsBoolean("Split", "s", "When using hue nesting with a variable that takes two levels, "
                                     "set to True for easier distributions comparison"),
        hs.HopsBoolean("Dodge", "d", "When hue nesting is used, whether elements should be shifted "
                                     "along the categorical axis"),
        hs.HopsString("Palette", "p", "Seaborn palette for your graph."
                                      "\nInput a valid name or select one from the output of the 'preset' component"
                                      "\nDefault = 'deep'"),
        hs.HopsBoolean("Plot", "P", "Plot me!")
    ],
    outputs=[
        hs.HopsString("Base64 png", "img_str", "Image as base64 bitmap."),
    ]
)
def violin_df(csv_df1: str, x_ax, y_ax, g_hue='', g_bw=1, g_inner="box", g_split=False, g_dodge=True, g_palette="deep",
              plot: bool = False):
    # load csv to df
    the_dataframe = csv_to_df(csv_df1)
    if plot:
        return all_graphs.violin(the_dataframe, x_ax, y_ax, g_hue, g_bw, g_inner, g_split, g_dodge, g_palette)


@hops.component(
    "/boxenplot",
    name="dataframes boxenploter",
    nickname="boxenDF",
    description="Boxenplot a dataframe",
    inputs=[
        hs.HopsString("Dataframe", "Df", "Dataframe to boxenplot"),
        hs.HopsString("X axis", "X", "What's your X value?"),
        hs.HopsString("Y axis", "Y", "What's your Y value? Has to refer to numerical values"),
        hs.HopsString("Hue", "h", "Column value to differentiate X and Y with"),
        hs.HopsBoolean("Dodge", "d", "When hue nesting is used, whether elements should be shifted "
                                     "along the categorical axis"),
        hs.HopsString("K depth", "k", "The number of boxes, and by extension number of percentiles, to draw"
                                      "\nChoose from: 'tukey', 'proportion', trustworthy', or 'full'"
                                      "\nDefault = 'tukey'"),
        hs.HopsString("Palette", "p", "Seaborn palette for your graph."
                                      "\nInput a valid name or select one from the output of the 'preset' component"
                                      "\nDefault = 'deep'"),
        hs.HopsBoolean("Fliers", "f", "Show fliers, Default = True"),
        hs.HopsBoolean("Plot", "P", "Plot me!")
    ],
    outputs=[
        hs.HopsString("Base64 png", "img_str", "Image as base64 bitmap."),
    ]
)
def boxen_df(csv_df1: str, x_ax, y_ax, g_hue='', g_dodge=True, g_k_depth="tukey", g_palette="deep", g_showfliers=True,
             plot: bool = False):
    # load csv to df
    the_dataframe = csv_to_df(csv_df1)
    if plot:
        return all_graphs.boxen(the_dataframe, x_ax, y_ax, g_hue, g_dodge, g_k_depth, g_palette, g_showfliers)


@hops.component(
    "/pointplot",
    name="dataframes pointploter",
    nickname="pointDF",
    description="Pointplot a dataframe",
    inputs=[
        hs.HopsString("Dataframe", "Df", "Dataframe to pointplot"),
        hs.HopsString("X axis", "X", "What's your X value?"),
        hs.HopsString("Y axis", "Y", "What's your Y value? Has to refer to numerical values"),
        hs.HopsString("Hue", "h", "Column value to differentiate X and Y with"),
        hs.HopsBoolean("Dodge", "d", "When hue nesting is used, whether elements should be shifted "
                                     "along the categorical axis"),
        hs.HopsBoolean("Join", "j", "If True, lines will be drawn between point estimates at the same hue level"),
        hs.HopsNumber("Scale", "s", "Scale factor for the plot elements"),
        hs.HopsNumber("Error width", "e", "Thickness of error bar lines"),
        hs.HopsString("Palette", "p", "Seaborn palette for your graph."
                                      "\nInput a valid name or select one from the output of the 'preset' component"
                                      "\nDefault = 'deep'"),
        hs.HopsBoolean("Plot", "P", "Plot me!")
    ],
    outputs=[
        hs.HopsString("Base64 png", "img_str", "Image as base64 bitmap."),
    ]
)
def point_df(csv_df1: str, x_ax, y_ax, g_hue='', g_dodge=False, g_join=True, g_scale=1, g_errwidth=0, g_palette='deep',
             plot: bool = False):
    # load csv to df
    the_dataframe = csv_to_df(csv_df1)
    if plot:
        return all_graphs.point(the_dataframe, x_ax, y_ax, g_hue, g_dodge, g_join, g_scale, g_errwidth, g_palette)


@hops.component(
    "/barplot",
    name="dataframes barploter",
    nickname="barDF",
    description="Barplot a dataframe",
    inputs=[
        hs.HopsString("Dataframe", "Df", "Dataframe to barplot"),
        hs.HopsString("X axis", "X", "What's your X value?"),
        hs.HopsString("Y axis", "Y", "What's your Y value? Has to refer to numerical values"),
        hs.HopsString("Hue", "h", "Column value to differentiate X and Y with"),
        hs.HopsString("ci", "c", "Confidence interval can be set to 'sd' as for 'standard deviation'"),
        hs.HopsNumber("Error width", "e", "Thickness of error bar lines"),
        hs.HopsString("Palette", "p", "Seaborn palette for your graph."
                                      "\nInput a valid name or select one from the output of the 'preset' component"
                                      "\nDefault = 'deep'"),
        hs.HopsBoolean("Plot", "P", "Plot me!")
    ],
    outputs=[
        hs.HopsString("Base64 png", "img_str", "Image as base64 bitmap."),
    ]
)
def bar_df(csv_df1: str, x_ax, y_ax, g_hue='', g_ci="sd", g_errwidth=0, g_palette="deep", plot: bool = False):
    # load csv to df
    the_dataframe = csv_to_df(csv_df1)
    if plot:
        return all_graphs.bar(the_dataframe, x_ax, y_ax, g_hue, g_ci, g_errwidth, g_palette)


@hops.component(
    "/countplot",
    name="dataframes countploter",
    nickname="barDF",
    description="Countplot a dataframe",
    inputs=[
        hs.HopsString("Dataframe", "Df", "Dataframe to countplot"),
        hs.HopsString("X axis", "X", "What's your X value?"),
        hs.HopsString("Hue", "h", "Column value to differentiate X and Y with"),
        hs.HopsBoolean("Dodge", "d", "When hue nesting is used, whether elements should be shifted "
                                     "along the categorical axis"),
        hs.HopsString("Palette", "p", "Seaborn palette for your graph."
                                      "\nInput a valid name or select one from the output of the 'preset' component"
                                      "\nDefault = 'deep'"),
        hs.HopsBoolean("Plot", "P", "Plot me!")
    ],
    outputs=[
        hs.HopsString("Base64 png", "img_str", "Image as base64 bitmap."),
    ]
)
def count_df(csv_df1: str, x_ax, g_hue='', g_dodge=True, g_palette="deep", plot: bool=False):
    # load csv to df
    the_dataframe = csv_to_df(csv_df1)
    if plot:
        return all_graphs.count(the_dataframe, x_ax, g_hue, g_dodge, g_palette)


# ----------------------------------------------------------------------------------


if __name__ == "__main__":
    # app.run(debug=False)
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
    
    # app.run(host="0.0.0.0", port= 5000, debug=False)
