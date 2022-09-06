from email.policy import default
from flask import Flask
import ghhops_server as hs
import pandas as pd
import os
import json

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
        hs.HopsString("Data as tree", "Dt",
                      "Data tree to convert", hs.HopsParamAccess.TREE),
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
        hs.HopsString("Available plots", "Plots",
                      "Currently available plots", hs.HopsParamAccess.LIST),
        hs.HopsString("Available palettes", "Palettes",
                      "Currently available palettes", hs.HopsParamAccess.LIST)
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
def json_parser(*json_str):

    return [json.loads(f) for f in json_str]
# ---------------------------------
# RELATIONAL PLOTS


@hops.component(
    "/relplot",
    name="dataframes relploter",
    nickname="relDF",
    description="Relplot a dataframe",
    inputs=[
        hs.HopsString("Dataframe", "df", "Dataframe to relplot"),
        hs.HopsString("X axis", "x", "What's your X value?"),
        hs.HopsString(
            "Y axis", "y", "What's your Y value? Has to refer to numerical values"),
        hs.HopsString(
            "Hue", "hue", "Column value to differentiate X and Y with"),
        hs.HopsString("Size", "size", "Grouping variable that will produce elements with different sizes. Can be either categorical or numeric,"),
        hs.HopsString("Style", "style", "Grouping variable that will produce elements with different styles. Can have a numeric dtype but will always be treated as categorical."),
        hs.HopsString("Rows", "row", "Variables that define subsets to plot on different facets."),
        hs.HopsString("Columns", "col", "Variables that define subsets to plot on different facets."),
        hs.HopsString("Wrap", "col_wrap", "“Wrap” the column variable at this width, so that the column facets span multiple rows", default=''),
        hs.HopsString("Kind", "kind", "Options are 'scatter' and 'line'}.", default = "scatter"),
        hs.HopsString("Palette", "palette", "Seaborn palette for your graph."
                      "\nInput a valid name or select one from the output of the 'preset' component"
                      "\nDefault = 'deep'", default= 'deep'),
        hs.HopsString("Figure Size", "fig_size", "String 'width; height' in inches", default=''),
        hs.HopsString("Despine", "despine",
                      "Despine your graph. Choose from: 'True', 'False', 'left', 'right', 'top'", default='{}'),
        hs.HopsString("Additional Arguments", "add_args",
                      "Additional seaborn plot arguments passed as a JSON Object", default='{}'),
        hs.HopsString("Axis Arguments", "ax_args",
                      "Additional matplotlib axis  arguments passed as a JSON Object", default='{}'),
        hs.HopsBoolean("Plot", "Plot", "Plot me!")
    ],
    outputs=[
        hs.HopsString("Base64 png", "img_str", "Image as base64 bitmap."),
    ]
)
def rel_df(csv_df1: str, x_ax, y_ax, g_hue='', g_size = '', g_style='', g_row='', g_col= '', g_col_wrap='', g_kind = 'scatter', g_palette="deep",  g_fig_size='', g_despine='{}', g_add_args='{}', g_ax_args='{}', plot: bool = False):
    # load csv to df
    the_dataframe = csv_to_df(csv_df1)

    g_despine, g_add_args, g_ax_args = json_parser(
        g_despine, g_add_args, g_ax_args)

    if plot:
        return all_graphs.rel(the_dataframe, x_ax, y_ax, g_hue, g_size, g_style, g_row, g_col,g_col_wrap, g_kind, g_palette, g_fig_size, g_despine, g_add_args, g_ax_args)


@hops.component(
    "/scatterplot",
    name="dataframes scatterploter",
    nickname="scatterDF",
    description="Scatterplot a dataframe",
    inputs=[
        hs.HopsString("Dataframe", "df", "Dataframe to scatterplot"),
        hs.HopsString("X axis", "x", "What's your X value?"),
        hs.HopsString(
            "Y axis", "y", "What's your Y value? Has to refer to numerical values"),
        hs.HopsString(
            "Hue", "hue", "Column value to differentiate X and Y with"),
        hs.HopsString("Palette", "palette", "Seaborn palette for your graph."
                      "\nInput a valid name or select one from the output of the 'preset' component"
                      "\nDefault = 'deep'"),
        hs.HopsString("Figure Size", "fig_size", "String 'width; height' in inches", default=''),
        hs.HopsString("Despine", "despine",
                      "Despine your graph. Choose from: 'True', 'False', 'left', 'right', 'top'", default='{}'),
        hs.HopsString("Additional Arguments", "add_args",
                      "Additional seaborn plot arguments passed as a JSON Object", default='{}'),
        hs.HopsString("Axis Arguments", "ax_args",
                      "Additional matplotlib axis  arguments passed as a JSON Object", default='{}'),
        hs.HopsBoolean("Plot", "Plot", "Plot me!")
    ],
    outputs=[
        hs.HopsString("Base64 png", "img_str", "Image as base64 bitmap."),
    ]
)
def scatter_df(csv_df1: str, x_ax, y_ax, g_hue='', g_palette="deep", g_fig_size='', g_despine='{}', g_add_args='{}', g_ax_args='{}', plot: bool = False):
    # load csv to df
    the_dataframe = csv_to_df(csv_df1)
    
    g_despine, g_add_args, g_ax_args = json_parser(
    g_despine, g_add_args, g_ax_args)
    
    if plot:
        return all_graphs.scatter(the_dataframe, x_ax, y_ax, g_hue, g_palette, g_fig_size, g_despine, g_add_args, g_ax_args)


@hops.component(
    "/lineplot",
    name="dataframes lineploter",
    nickname="lineDF",
    description="Lineplot a dataframe",
    inputs=[
        hs.HopsString("Dataframe", "df", "Dataframe to lineplot"),
        hs.HopsString("X axis", "x", "What's your X value?"),
        hs.HopsString(
            "Y axis", "y", "What's your Y value? Has to refer to numerical values"),
        hs.HopsString(
            "Hue", "hue", "Column value to differentiate X and Y with"),
        hs.HopsString("Palette", "palette", "Seaborn palette for your graph."
                      "\nInput a valid name or select one from the output of the 'preset' component"
                      "\nDefault = 'deep'"),
        hs.HopsString("Figure Size", "fig_size", "String 'width; height' in inches", default=''),
        hs.HopsString("Despine", "despine",
                      "Despine your graph. Choose from: 'True', 'False', 'left', 'right', 'top'", default='{}'),
        hs.HopsString("Additional Arguments", "add_args",
                      "Additional seaborn plot arguments passed as a JSON Object", default='{}'),
        hs.HopsString("Axis Arguments", "ax_args",
                      "Additional matplotlib axis  arguments passed as a JSON Object", default='{}'),
        hs.HopsBoolean("Plot", "Plot", "Plot me!")
    ],
    outputs=[
        hs.HopsString("Base64 png", "img_str", "Image as base64 bitmap."),
    ]
)
def line_df(csv_df1: str, x_ax, y_ax, g_hue='', g_palette="deep", g_fig_size='', g_despine='{}', g_add_args='{}', g_ax_args='{}', plot: bool = False):
    # load csv to df
    the_dataframe = csv_to_df(csv_df1)
    
    g_despine, g_add_args, g_ax_args = json_parser(
    g_despine, g_add_args, g_ax_args)
    
    if plot:
        return all_graphs.line(the_dataframe, x_ax, y_ax, g_hue, g_palette, g_fig_size, g_despine, g_add_args, g_ax_args)


# ------------------------------------------------r
# DISTRIBUTION PLOTS


@hops.component(
    "/displot",
    name="dataframes disploter",
    nickname="disDF",
    description="Displot a dataframe in one dimension",
    inputs=[
        hs.HopsString("Dataframe", "df", "Dataframe to displot"),
        hs.HopsString("X axis", "x", "What's your X value?"),
        hs.HopsString("Y axis", "Y", "What's your Y value?"),
        hs.HopsString(
            "Hue", "hue", "Column value to differentiate X and Y with"),
          hs.HopsString("Rows", "row", "Variables that define subsets to plot on different facets."),
        hs.HopsString("Columns", "col", "Variables that define subsets to plot on different facets."),
        hs.HopsString("Wrap", "col_wrap", "“Wrap” the column variable at this width, so that the column facets span multiple rows", default=''),
        hs.HopsString("Kind", "kind", "Selects the underlying plotting function and determines the additional set of "
                                   "valid parameters.\nChoose from 'hist', 'kde' or 'ecdf' \nDefault: 'hist'", default='hist'),
        hs.HopsBoolean(
            "Rug", "rug", "If True, show each observation with marginal ticks"),
        hs.HopsBoolean(
            "Legend", "legend", "If False, suppress the legend for semantic variables"),
        hs.HopsString("Palette", "palette", "Seaborn palette for your graph."
                      "\nInput a valid name or select one from the output of the 'preset' component"
                      "\nDefault = 'deep'"),
        hs.HopsString("Figure Size", "fig_size", "String 'width; height' in inches", default=''),
        hs.HopsString("Despine", "despine",
                      "Despine your graph. Choose from: 'True', 'False', 'left', 'right', 'top'", default='{}'),
        hs.HopsString("Additional Arguments", "add_args",
                      "Additional seaborn plot arguments passed as a JSON Object", default='{}'),
        hs.HopsString("Axis Arguments", "ax_args",
                      "Additional matplotlib axis  arguments passed as a JSON Object", default='{}'),
        hs.HopsBoolean("Plot", "Plot", "Plot me!")
    ],
    outputs=[
        hs.HopsString("Base64 png", "img_str", "Image as base64 bitmap."),
    ]
)
def dis_df(csv_df1: str, x_ax, y_ax='', g_hue='', g_row='', g_col= '', g_col_wrap='', g_kind='hist', g_rug=False, g_legend=True, g_palette="deep", g_fig_size='', g_despine='{}', g_add_args='{}', g_ax_args='{}',
           plot: bool = False):
    # load csv to df
    the_dataframe = csv_to_df(csv_df1)

    g_despine, g_add_args, g_ax_args = json_parser(
    g_despine, g_add_args, g_ax_args)

    if plot:
        return all_graphs.dis(the_dataframe, x_ax, y_ax, g_hue, g_row, g_col,g_col_wrap, g_kind, g_rug, g_legend, g_palette, g_fig_size, g_despine, g_add_args, g_ax_args)


@hops.component(
    "/histplot",
    name="dataframes histploter",
    nickname="histDF_1",
    description="Histplot a dataframe",
    inputs=[
        hs.HopsString("Dataframe", "df", "Dataframe to histplot"),
        hs.HopsString("X axis", "x", "What's your X value?"),
        hs.HopsString("Y axis", "y", "What's your Y value? (optional)"),
        hs.HopsString(
            "Hue", "hue", "Column value to differentiate X and Y with"),
        hs.HopsString("Stat", "stat", "Aggregate statistic to compute in each bin"
                                   "\nChoose from 'count', 'frequency', 'probability', 'percent' or 'density'"
                                   "\nDefault: 'count'"),
        hs.HopsBoolean("Cumulative", "cumulative",
                       "If True, plot the cumulative counts as bins increase."),
        hs.HopsString("Multiple", "multiple", "Approach to resolving multiple elements when semantic mapping creates subsets. "
                                       "Only relevant with univariate data"
                                       "\nChoose from 'layer', 'dodge', 'stack', 'fill' \nDefault: 'layer'"),
        hs.HopsString("Element", "element", "Visual representation of the histogram statistic. Only relevant with univariate "
                                      "data \nChoose from 'bars', 'step' or 'poly' \nDefault: 'bars'"),
        hs.HopsBoolean("Fill", "fill", "If True, fill in the space under the histogram. Only relevant with "
                                    "univariate data."),
        hs.HopsNumber("Shrink", "shrink", "Scale the width of each bar relative to the binwidth by this factor."
                                     "Only relevant with univariate data"),
        hs.HopsBoolean("KDE", "kde", "If True, compute a kernel density estimate to smooth the distribution and show on "
                                   "the plot as (one or more) line(s). Only relevant with univariate data."),
        hs.HopsBoolean(
            "Legend", "legend", "If False, suppress the legend for semantic variables"),
        hs.HopsString("Palette", "palette", "Seaborn palette for your graph."
                      "\nInput a valid name or select one from the output of the 'preset' component"
                      "\nDefault = 'deep'"),
        hs.HopsString("Figure Size", "fig_size", "String 'width; height' in inches", default=''),
        hs.HopsString("Despine", "despine",
                      "Despine your graph. Choose from: 'True', 'False', 'left', 'right', 'top'", default='{}'),
        hs.HopsString("Additional Arguments", "add_args",
                      "Additional seaborn plot arguments passed as a JSON Object", default='{}'),
        hs.HopsString("Axis Arguments", "ax_args",
                      "Additional matplotlib axis  arguments passed as a JSON Object", default='{}'),
        hs.HopsBoolean("Plot", "Plot", "Plot me!")
    ],
    outputs=[
        hs.HopsString("Base64 png", "img_str", "Image as base64 bitmap."),
    ]
)
def hist_df(csv_df1: str, x_ax, y_ax='', g_hue='', g_stat='count', g_cumulative=False, g_multiple='layer',
            g_element='bars', g_fill=True, g_shrink=1, g_kde=False, g_legend=True, g_palette="deep", g_fig_size='', g_despine='{}', g_add_args='{}', g_ax_args='{}',
            plot: bool = False):

    # load csv to df
    the_dataframe = csv_to_df(csv_df1)

    g_despine, g_add_args, g_ax_args = json_parser(
    g_despine, g_add_args, g_ax_args)

    if plot:
        return all_graphs.hist(the_dataframe, x_ax, y_ax, g_hue, g_stat, g_cumulative, g_multiple, g_element, g_fill, g_shrink,
                               g_kde, g_legend, g_palette, g_fig_size, g_despine, g_add_args, g_ax_args)


@hops.component(
    "/kdeplot",
    name="dataframes kdeploter",
    nickname="kdeDF",
    description="Kdeplot a dataframe",
    inputs=[
        hs.HopsString("Dataframe", "df", "Dataframe to kdeplot"),
        hs.HopsString(
            "X axis", "x", "What's your X value? Has to be numerical"),
        hs.HopsString(
            "Y axis", "y", "What's your Y value? Has to be numerical (but is optional)"),
        hs.HopsString(
            "Hue", "hue", "Column value to differentiate X and Y with"),
        hs.HopsNumber("Cut", "cut", "Factor, multiplied by the smoothing bandwidth, that determines how far the "
                                  "evaluation grid extends past the extreme datapoints. "
                                  "\nWhen set to 0, truncate the curve at the data limits."),
        hs.HopsBoolean("Cumulative", "cumulative",
                       "If True, estimate a cumulative distribution function"),
        hs.HopsString("Multiple", "multiple", "Approach to resolving multiple elements when semantic mapping creates subsets. "
                                       "Only relevant with univariate data"
                                       "\nChoose from 'layer', 'stack', 'fill' \nDefault: 'layer'"),
        hs.HopsBoolean("Common norm", "common_norm", "If True, scale each conditional density by the number of observations such"
                                            "that the total area under all densities sums to 1. "
                                            "\nOtherwise, normalize each density independently."),
        hs.HopsBoolean("Common grid", "common_grid", "If True, use the same evaluation grid for each kernel density estimate. "
                                            "\nOnly relevant with univariate data."),
        hs.HopsInteger("Levels", "levels", "Number of contour levels or values to draw contours at."
                                      "\nLevels correspond to iso-proportions of the density: e.g., 20% of the "
                                      "probability mass will lie below the contour drawn for 0.2. Only relevant with "
                                      "bivariate data."),
        hs.HopsNumber("Thresh", "thresh", "Lowest iso-proportion level at which to draw a contour line. Ignored when levels "
                                     "is a vector. Only relevant with bivariate data."),
        hs.HopsNumber("Alpha", "alpha", "Alpha value for the fill option"),
        hs.HopsBoolean("Fill", "fill", "Fill ?"),
        hs.HopsBoolean(
            "Legend", "legend", "If False, suppress the legend for semantic variables"),
        hs.HopsString("Palette", "palette", "Seaborn palette for your graph."
                      "\nInput a valid name or select one from the output of the 'preset' component"
                      "\nDefault = 'deep'"),
        hs.HopsString("Figure Size", "fig_size", "String 'width; height' in inches", default=''),
        hs.HopsString("Despine", "despine",
                      "Despine your graph. Choose from: 'True', 'False', 'left', 'right', 'top'", default='{}'),
        hs.HopsString("Additional Arguments", "add_args",
                      "Additional seaborn plot arguments passed as a JSON Object", default='{}'),
        hs.HopsString("Axis Arguments", "ax_args",
                      "Additional matplotlib axis  arguments passed as a JSON Object", default='{}'),
        hs.HopsBoolean("Plot", "Plot", "Plot me!")
    ],
    outputs=[
        hs.HopsString("Base64 png", "img_str", "Image as base64 bitmap."),
    ]
)
def kde_df(csv_df1: str, x_ax, y_ax='', g_hue='', g_cut=3, g_cumulative=False, g_multiple='layer', g_common_norm=True,
           g_common_grid=False, g_levels=10, g_thresh=0.05, g_alpha=1, g_fill=False, g_legend=True,
           g_palette="deep", g_fig_size='', g_despine='{}', g_add_args='{}', g_ax_args='{}', plot: bool = False):
    # load csv to df
    the_dataframe = csv_to_df(csv_df1)

    g_despine, g_add_args, g_ax_args = json_parser(
    g_despine, g_add_args, g_ax_args)

    if plot:
        return all_graphs.kde(the_dataframe, x_ax, y_ax, g_hue, g_cut, g_cumulative, g_multiple, g_common_norm, g_common_grid,
                              g_levels, g_thresh, g_alpha, g_fill, g_legend, g_palette, g_fig_size, g_despine, g_add_args, g_ax_args)


# -------------------------------------------------
# CATEGORICAL PLOTS


@hops.component(
    "/catplot",
    name="dataframes catploter",
    nickname="catDF",
    description="Catplot a dataframe",
    inputs=[
        hs.HopsString("Dataframe", "df", "Dataframe to catplot"),
        hs.HopsString("X axis", "x", "What's your X value?"),
        hs.HopsString(
            "Y axis", "y", "What's your Y value? Has to refer to numerical values"),
        hs.HopsString(
            "Hue", "hue", "Column value to differentiate X and Y with"),
        hs.HopsString("Rows", "row", "Variables that define subsets to plot on different facets."),
        hs.HopsString("Columns", "col", "Variables that define subsets to plot on different facets."),
        hs.HopsString("Wrap", "col_wrap", "“Wrap” the column variable at this width, so that the column facets span multiple rows", default=''),
        hs.HopsString(
            "Coinfidence Interval", "ci", "Confidence interval can be set to 'sd' as for 'standard deviation'"),
        hs.HopsInteger("Seed", "seed", "Seed for reproducible bootstrapping"),
        hs.HopsString("Kind", "kind", "The kind of plot to draw, corresponds to the name of a categorical axes-level "
                                   "plotting function"
                                   "\nChoose from: 'strip', 'swarm', 'box', 'violin', 'boxen', 'point', 'bar', "
                                   "or 'count'"
                                   "\nDefault = 'strip'"),
        hs.HopsString("Palette", "palette", "Seaborn palette for your graph."
                      "\nInput a valid name or select one from the output of the 'preset' component"
                      "\nDefault = 'deep'"),
        hs.HopsString("Figure Size", "fig_size", "String 'width; height' in inches", default=''),
        hs.HopsString("Despine", "despine",
                      "Despine your graph. Choose from: 'True', 'False', 'left', 'right', 'top'", default='{}'),
        hs.HopsString("Additional Arguments", "add_args",
                      "Additional seaborn plot arguments passed as a JSON Object", default='{}'),
        hs.HopsString("Axis Arguments", "ax_args",
                      "Additional matplotlib axis  arguments passed as a JSON Object", default='{}'),
        hs.HopsBoolean("Plot", "Plot", "Plot me!")
    ],
    outputs=[
        hs.HopsString("Base64 png", "img_str", "Image as base64 bitmap."),
    ]
)
def cat_df(csv_df1: str, x_ax, y_ax, g_hue='', g_row='', g_col= '', g_col_wrap='', g_ci="None", g_seed=2, g_kind="strip", g_palette="deep", g_fig_size='', g_despine='{}', g_add_args='{}', g_ax_args='{}',
           plot: bool = False):
    # load csv to df
    the_dataframe = csv_to_df(csv_df1)

    g_despine, g_add_args, g_ax_args = json_parser(
    g_despine, g_add_args, g_ax_args)

    if plot:
        return all_graphs.cat(the_dataframe, x_ax, y_ax, g_hue, g_row, g_col,g_col_wrap, g_ci, g_seed, g_kind, g_palette, g_fig_size, g_despine, g_add_args, g_ax_args)


@hops.component(
    "/stripplot",
    name="dataframes stripploter",
    nickname="stripDF",
    description="Stripplot a dataframe",
    inputs=[
        hs.HopsString("Dataframe", "df", "Dataframe to stripplot"),
        hs.HopsString("X axis", "x", "What's your X value?"),
        hs.HopsString(
            "Y axis", "y", "What's your Y value? Has to refer to numerical values"),
        hs.HopsString(
            "Hue", "hue", "Column value to differentiate X and Y with"),
        hs.HopsNumber(
            "Jitter", "jitter", "Amount of jitter (only along the categorical axis) to apply"),
        hs.HopsNumber("Size", "marker_size", "Radius of the markers, in points"),
        hs.HopsString("Palette", "palette", "Seaborn palette for your graph."
                      "\nInput a valid name or select one from the output of the 'preset' component"
                      "\nDefault = 'deep'"),
        hs.HopsString("Figure Size", "fig_size", "String 'width; height' in inches", default=''),
        hs.HopsString("Despine", "despine",
                      "Despine your graph. Choose from: 'True', 'False', 'left', 'right', 'top'", default='{}'),
        hs.HopsString("Additional Arguments", "add_args",
                      "Additional seaborn plot arguments passed as a JSON Object", default='{}'),
        hs.HopsString("Axis Arguments", "ax_args",
                      "Additional matplotlib axis  arguments passed as a JSON Object", default='{}'),
        hs.HopsBoolean("Plot", "Plot", "Plot me!")
    ],
    outputs=[
        hs.HopsString("Base64 png", "img_str", "Image as base64 bitmap."),
    ]
)
def strip_df(csv_df1: str, x_ax, y_ax, g_hue='', g_jitter=True, g_size=2, g_palette="deep", g_fig_size='', g_despine='{}', g_add_args='{}', g_ax_args='{}', plot: bool = False):
    # load csv to df
    the_dataframe = csv_to_df(csv_df1)

    g_despine, g_add_args, g_ax_args = json_parser(
    g_despine, g_add_args, g_ax_args)

    if plot:
        return all_graphs.strip(the_dataframe, x_ax, y_ax, g_hue, g_jitter, g_size, g_palette , g_fig_size, g_despine, g_add_args, g_ax_args)


@hops.component(
    "/swarmplot",
    name="dataframes swarmploter",
    nickname="swarmDF",
    description="Swarmplot a dataframe",
    inputs=[
        hs.HopsString("Dataframe", "df", "Dataframe to swarmplot"),
        hs.HopsString("X axis", "x", "What's your X value?"),
        hs.HopsString(
            "Y axis", "y", "What's your Y value? Has to refer to numerical values"),
        hs.HopsString(
            "Hue", "hue", "Column value to differentiate X and Y with"),
        hs.HopsBoolean("Dodge", "dodge", "Setting this to True will separate the strips for different hue levels along "
                                     "the categorical axis"),
        hs.HopsNumber("Size", "marker_size", "Radius of the markers, in points"),
        hs.HopsString("Palette", "palette", "Seaborn palette for your graph."
                      "\nInput a valid name or select one from the output of the 'preset' component"
                      "\nDefault = 'deep'"),
        hs.HopsString("Figure Size", "fig_size", "String 'width; height' in inches", default=''),
        hs.HopsString("Despine", "despine",
                      "Despine your graph. Choose from: 'True', 'False', 'left', 'right', 'top'", default='{}'),
        hs.HopsString("Additional Arguments", "add_args",
                      "Additional seaborn plot arguments passed as a JSON Object", default='{}'),
        hs.HopsString("Axis Arguments", "ax_args",
                      "Additional matplotlib axis  arguments passed as a JSON Object", default='{}'),
        hs.HopsBoolean("Plot", "Plot", "Plot me!")
    ],
    outputs=[
        hs.HopsString("Base64 png", "img_str", "Image as base64 bitmap."),
    ]
)
def swarm_df(csv_df1: str, x_ax, y_ax, g_hue='', g_dodge=False, g_size=2,g_palette="deep", g_fig_size='', g_despine='{}', g_add_args='{}', g_ax_args='{}', plot: bool = False):
    # load csv to df
    the_dataframe = csv_to_df(csv_df1)

    g_despine, g_add_args, g_ax_args = json_parser(
    g_despine, g_add_args, g_ax_args)

    if plot:
        return all_graphs.swarm(the_dataframe, x_ax, y_ax, g_hue, g_dodge, g_size, g_palette, g_fig_size, g_despine, g_add_args, g_ax_args)


@hops.component(
    "/boxplot",
    name="dataframes boxploter",
    nickname="boxDF",
    description="Boxplot a dataframe",
    inputs=[
        hs.HopsString("Dataframe", "df", "Dataframe to boxplot"),
        hs.HopsString("X axis", "x", "What's your X value?"),
        hs.HopsString(
            "Y axis", "y", "What's your Y value? Has to refer to numerical values"),
        hs.HopsString(
            "Hue", "hue", "Column value to differentiate X and Y with"),
        hs.HopsString("Palette", "palette", "Seaborn palette for your graph."
                      "\nInput a valid name or select one from the output of the 'preset' component"
                      "\nDefault = 'deep'"),
        hs.HopsString("Figure Size", "fig_size", "String 'width; height' in inches", default=''),
        hs.HopsString("Despine", "despine",
                      "Despine your graph. Choose from: 'True', 'False', 'left', 'right', 'top'", default='{}'),
        hs.HopsString("Additional Arguments", "add_args",
                      "Additional seaborn plot arguments passed as a JSON Object", default='{}'),
        hs.HopsString("Axis Arguments", "ax_args",
                      "Additional matplotlib axis  arguments passed as a JSON Object", default='{}'),
        hs.HopsBoolean("Plot", "Plot", "Plot me!")
    ],
    outputs=[
        hs.HopsString("Base64 png", "img_str", "Image as base64 bitmap."),
    ]
)
def box_df(csv_df1: str, x_ax, y_ax, g_hue='', g_palette="deep", g_fig_size='', g_despine='{}', g_add_args='{}', g_ax_args='{}', plot: bool = False):
    # load csv to df
    the_dataframe = csv_to_df(csv_df1)

    g_despine, g_add_args, g_ax_args = json_parser(
    g_despine, g_add_args, g_ax_args)

    if plot:
        img = all_graphs.box(the_dataframe, x_ax, y_ax, g_hue, g_palette, g_fig_size, g_despine, g_add_args, g_ax_args)
        return img


@hops.component(
    "/violinplot",
    name="dataframes violinploter",
    nickname="violinDF",
    description="Violinplot a dataframe",
    inputs=[
        hs.HopsString("Dataframe", "df", "Dataframe to violinplot"),
        hs.HopsString("X axis", "x", "What's your X value?"),
        hs.HopsString(
            "Y axis", "y", "What's your Y value? Has to refer to numerical values"),
        hs.HopsString(
            "Hue", "hue", "Column value to differentiate X and Y with"),
        hs.HopsNumber(
            "bw", "b", "The scale factor to use when computing the kernel bandwidth"),
        hs.HopsString("Inner", "inner", "Representation of the datapoints in the violin interior"
                                    "\nChoose from 'box', 'quartile', 'point', or 'stick'"
                                    "\nDefault = 'box'"),
        hs.HopsBoolean("Split", "split", "When using hue nesting with a variable that takes two levels, "
                                     "set to True for easier distributions comparison"),
        hs.HopsBoolean("Dodge", "dodge", "When hue nesting is used, whether elements should be shifted "
                                     "along the categorical axis"),
        hs.HopsString("Palette", "palette", "Seaborn palette for your graph."
                      "\nInput a valid name or select one from the output of the 'preset' component"
                      "\nDefault = 'deep'"),
        hs.HopsString("Figure Size", "fig_size", "String 'width; height' in inches", default=''),
        hs.HopsString("Despine", "despine",
                      "Despine your graph. Choose from: 'True', 'False', 'left', 'right', 'top'", default='{}'),
        hs.HopsString("Additional Arguments", "add_args",
                      "Additional seaborn plot arguments passed as a JSON Object", default='{}'),
        hs.HopsString("Axis Arguments", "ax_args",
                      "Additional matplotlib axis  arguments passed as a JSON Object", default='{}'),
        hs.HopsBoolean("Plot", "Plot", "Plot me!")
    ],
    outputs=[
        hs.HopsString("Base64 png", "img_str", "Image as base64 bitmap."),
    ]
)
def violin_df(csv_df1: str, x_ax, y_ax, g_hue='', g_bw=1, g_inner="box", g_split=False, g_dodge=True, g_palette="deep", g_fig_size='', g_despine='{}', g_add_args='{}', g_ax_args='{}',
              plot: bool = False):
    # load csv to df
    the_dataframe = csv_to_df(csv_df1)

    g_despine, g_add_args, g_ax_args = json_parser(
    g_despine, g_add_args, g_ax_args)

    if plot:
        return all_graphs.violin(the_dataframe, x_ax, y_ax, g_hue, g_bw, g_inner, g_split, g_dodge, g_palette, g_fig_size, g_despine, g_add_args, g_ax_args)


@hops.component(
    "/boxenplot",
    name="dataframes boxenploter",
    nickname="boxenDF",
    description="Boxenplot a dataframe",
    inputs=[
        hs.HopsString("Dataframe", "df", "Dataframe to boxenplot"),
        hs.HopsString("X axis", "x", "What's your X value?"),
        hs.HopsString(
            "Y axis", "y", "What's your Y value? Has to refer to numerical values"),
        hs.HopsString(
            "Hue", "hue", "Column value to differentiate X and Y with"),
        hs.HopsBoolean("Dodge", "dodge", "When hue nesting is used, whether elements should be shifted "
                                     "along the categorical axis"),
        hs.HopsString("K depth", "k_depth", "The number of boxes, and by extension number of percentiles, to draw"
                                      "\nChoose from: 'tukey', 'proportion', trustworthy', or 'full'"
                                      "\nDefault = 'tukey'"),
        hs.HopsBoolean("Fliers", "fliers", "Show fliers, Default = True"),
        hs.HopsString("Palette", "palette", "Seaborn palette for your graph."
                      "\nInput a valid name or select one from the output of the 'preset' component"
                      "\nDefault = 'deep'"),
        hs.HopsString("Figure Size", "fig_size", "String 'width; height' in inches", default=''),
        hs.HopsString("Despine", "despine",
                      "Despine your graph. Choose from: 'True', 'False', 'left', 'right', 'top'", default='{}'),
        hs.HopsString("Additional Arguments", "add_args",
                      "Additional seaborn plot arguments passed as a JSON Object", default='{}'),
        hs.HopsString("Axis Arguments", "ax_args",
                      "Additional matplotlib axis  arguments passed as a JSON Object", default='{}'),
        hs.HopsBoolean("Plot", "Plot", "Plot me!")
    ],
    outputs=[
        hs.HopsString("Base64 png", "img_str", "Image as base64 bitmap."),
    ]
)
def boxen_df(csv_df1: str, x_ax, y_ax, g_hue='', g_dodge=True, g_k_depth="tukey", g_showfliers=True, g_palette="deep", g_fig_size='', g_despine='{}', g_add_args='{}', g_ax_args='{}',
             plot: bool = False):
    # load csv to df
    the_dataframe = csv_to_df(csv_df1)

    g_despine, g_add_args, g_ax_args = json_parser(
    g_despine, g_add_args, g_ax_args)

    if plot:
        return all_graphs.boxen(the_dataframe, x_ax, y_ax, g_hue, g_dodge, g_k_depth, g_showfliers, g_palette, g_fig_size, g_despine, g_add_args, g_ax_args)


@hops.component(
    "/pointplot",
    name="dataframes pointploter",
    nickname="pointDF",
    description="Pointplot a dataframe",
    inputs=[
        hs.HopsString("Dataframe", "df", "Dataframe to pointplot"),
        hs.HopsString("X axis", "x", "What's your X value?"),
        hs.HopsString(
            "Y axis", "y", "What's your Y value? Has to refer to numerical values"),
        hs.HopsString(
            "Hue", "hue", "Column value to differentiate X and Y with"),
        hs.HopsBoolean("Dodge", "dodge", "When hue nesting is used, whether elements should be shifted "
                                     "along the categorical axis"),
        hs.HopsBoolean(
            "Join", "join", "If True, lines will be drawn between point estimates at the same hue level"),
        hs.HopsNumber("Scale", "scale", "Scale factor for the plot elements"),
        hs.HopsNumber("Error width", "error_width", "Thickness of error bar lines"),
        hs.HopsString("Palette", "palette", "Seaborn palette for your graph."
                      "\nInput a valid name or select one from the output of the 'preset' component"
                      "\nDefault = 'deep'"),
        hs.HopsString("Figure Size", "fig_size", "String 'width; height' in inches", default=''),
        hs.HopsString("Despine", "despine",
                      "Despine your graph. Choose from: 'True', 'False', 'left', 'right', 'top'", default='{}'),
        hs.HopsString("Additional Arguments", "add_args",
                      "Additional seaborn plot arguments passed as a JSON Object", default='{}'),
        hs.HopsString("Axis Arguments", "ax_args",
                      "Additional matplotlib axis  arguments passed as a JSON Object", default='{}'),
        hs.HopsBoolean("Plot", "Plot", "Plot me!")
    ],
    outputs=[
        hs.HopsString("Base64 png", "img_str", "Image as base64 bitmap."),
    ]
)
def point_df(csv_df1: str, x_ax, y_ax, g_hue='', g_dodge=False, g_join=True, g_scale=1, g_errwidth=0, g_palette='deep', g_fig_size='', g_despine='{}', g_add_args='{}', g_ax_args='{}',
             plot: bool = False):
    # load csv to df
    the_dataframe = csv_to_df(csv_df1)

    g_despine, g_add_args, g_ax_args = json_parser(
    g_despine, g_add_args, g_ax_args)

    if plot:
        return all_graphs.point(the_dataframe, x_ax, y_ax, g_hue, g_dodge, g_join, g_scale, g_errwidth, g_palette, g_fig_size, g_despine, g_add_args, g_ax_args)


@hops.component(
    "/barplot",
    name="dataframes barploter",
    nickname="barDF",
    description="Barplot a dataframe",
    inputs=[
        hs.HopsString("Dataframe", "df", "Dataframe to barplot"),
        hs.HopsString("X axis", "x", "What's your X value?"),
        hs.HopsString(
            "Y axis", "y", "What's your Y value? Has to refer to numerical values"),
        hs.HopsString(
            "Hue", "hue", "Column value to differentiate X and Y with"),
        hs.HopsString(
            "Confidence Interval", "ci", "Confidence interval can be set to 'sd' as for 'standard deviation'"),
        hs.HopsNumber("Error width", "error_width", "Thickness of error bar lines"),
        hs.HopsString("Palette", "palette", "Seaborn palette for your graph."
                      "\nInput a valid name or select one from the output of the 'preset' component"
                      "\nDefault = 'deep'"),
        hs.HopsString("Figure Size", "fig_size", "String 'width; height' in inches", default=''),
        hs.HopsString("Despine", "despine",
                      "Despine your graph. Choose from: 'True', 'False', 'left', 'right', 'top'", default='{}'),
        hs.HopsString("Additional Arguments", "add_args",
                      "Additional seaborn plot arguments passed as a JSON Object", default='{}'),
        hs.HopsString("Axis Arguments", "ax_args",
                      "Additional matplotlib axis  arguments passed as a JSON Object", default='{}'),
        hs.HopsBoolean("Plot", "Plot", "Plot me!")
    ],
    outputs=[
        hs.HopsString("Base64 png", "img_str", "Image as base64 bitmap."),
    ]
)
def bar_df(csv_df1: str, x_ax, y_ax, g_hue='', g_ci="sd", g_errwidth=0, g_palette="deep", g_fig_size='', g_despine='{}', g_add_args='{}', g_ax_args='{}', plot: bool = False):
    # load csv to df
    the_dataframe = csv_to_df(csv_df1)

    g_despine, g_add_args, g_ax_args = json_parser(
    g_despine, g_add_args, g_ax_args)

    if plot:
        return all_graphs.bar(the_dataframe, x_ax, y_ax, g_hue, g_ci, g_errwidth, g_palette, g_fig_size, g_despine, g_add_args, g_ax_args)


@hops.component(
    "/countplot",
    name="dataframes countploter",
    nickname="barDF",
    description="Countplot a dataframe",
    inputs=[
        hs.HopsString("Dataframe", "df", "Dataframe to countplot"),
        hs.HopsString("X axis", "x", "What's your X value?"),
        hs.HopsString(
            "Hue", "hue", "Column value to differentiate X and Y with"),
        hs.HopsBoolean("Dodge", "dodge", "When hue nesting is used, whether elements should be shifted "
                                     "along the categorical axis"),
        hs.HopsString("Palette", "palette", "Seaborn palette for your graph."
                      "\nInput a valid name or select one from the output of the 'preset' component"
                      "\nDefault = 'deep'"),
        hs.HopsString("Figure Size", "fig_size", "String 'width; height' in inches", default=''),
        hs.HopsString("Despine", "despine",
                      "Despine your graph. Choose from: 'True', 'False', 'left', 'right', 'top'", default='{}'),
        hs.HopsString("Additional Arguments", "add_args",
                      "Additional seaborn plot arguments passed as a JSON Object", default='{}'),
        hs.HopsString("Axis Arguments", "ax_args",
                      "Additional matplotlib axis  arguments passed as a JSON Object", default='{}'),
        hs.HopsBoolean("Plot", "Plot", "Plot me!")
    ],
    outputs=[
        hs.HopsString("Base64 png", "img_str", "Image as base64 bitmap."),
    ]
)
def count_df(csv_df1: str, x_ax, g_hue='', g_dodge=True, g_palette="deep", g_fig_size='', g_despine='{}', g_add_args='{}', g_ax_args='{}', plot: bool = False):
    # load csv to df
    the_dataframe = csv_to_df(csv_df1)

    g_despine, g_add_args, g_ax_args = json_parser(
    g_despine, g_add_args, g_ax_args)

    if plot:
        return all_graphs.count(the_dataframe, x_ax, g_hue, g_dodge, g_palette, g_fig_size, g_despine, g_add_args, g_ax_args)


# ----------------------------------------------------------------------------------


if __name__ == "__main__":
    # app.run(debug=False)
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

    # app.run(host="0.0.0.0", port= 5000, debug=False)
