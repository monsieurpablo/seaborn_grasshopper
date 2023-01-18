import base64
from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns
import io
import os

# TODO: Change this later
sns.set_style("ticks") # whitegrid, darkgrid, white, dark, ticks

def base64img():
    # https://stackoverflow.com/questions/37225035/serialize-in-json-a-base64-encoded-data
    my_stringIObytes = io.BytesIO()

    plt.savefig(my_stringIObytes, format='png', dpi=200)
    plt.close()

    my_stringIObytes.seek(0)
    imdata_bytes = base64.b64encode(my_stringIObytes.read())
    imdata_string = imdata_bytes.decode('utf-8')

    my_stringIObytes.flush()
    
    return imdata_string


def set_fig_size(g, fig_size):
    w, h = fig_size.split(';')
    # try:
    g.figure.set_figwidth(float(w))
    g.figure.set_figheight(float(h))
    # except:
        
def check_numeric(df,column):
    # try:
    if pd.api.types.is_numeric_dtype(df[column]):
        return True
    else:
        return False
        # raise ValueError(f"{column} does not contain numbers")
            
    # except ValueError as e:
    #     return e

def empty2none(args):
    for k, v in args.items():
        if type(v) == str:
            args[k] = None if v == '' else v
        if type(v) == int:
            args[k] = None if v == -999 else v
    return args


def clean_args(args):
    rm_list = ['add_args', 'ax_args', 'despine', 'fig_size']
    # remove optional args
    try:
        [args.pop(k) for k in rm_list]
    except:
        pass

    args = empty2none(args)
    
    # TODO check if string represents tuple or list (eval) ?

    return args

def example_data(data_base_name='iris'):
    # https://seaborn.pydata.org/generated/seaborn.load_dataset.html#seaborn.load_dataset
    sns.load_dataset(data_base_name).to_csv(index=False, line_terminator='@')


# ---------------------------------
# RELATIONAL PLOTS


def rel(data, x, y, hue, size, style, row, col, col_wrap, kind='scatter', palette='deep', fig_size ='', despine={}, add_args={}, ax_args={}):
    # https://seaborn.pydata.org/generated/seaborn.relplot.html#seaborn.relplot

    args = clean_args(locals())

    g = sns.relplot(**args, **add_args)
    g.set(**ax_args)

    if fig_size:
        set_fig_size(g, fig_size)

    if despine:
        sns.despine(**despine)

    # tight layout
    plt.tight_layout()

    return base64img()


def scatter(data, x, y, hue, palette, fig_size, despine={}, add_args={}, ax_args={}):
    # https://seaborn.pydata.org/generated/seaborn.scatterplot.html#seaborn.scatterplot

    args = clean_args(locals())

    g = sns.scatterplot(**args, **add_args)
    g.set(**ax_args)

    if fig_size:
        set_fig_size(g, fig_size)

    if despine:
        sns.despine(**despine)

    # tight layout
    plt.tight_layout()

    return base64img()


def line(data, x, y, hue, palette, fig_size, despine={}, add_args={}, ax_args={}):
    # https://seaborn.pydata.org/generated/seaborn.lineplot.html#seaborn.lineplot

    args = clean_args(locals())

    g = sns.lineplot(**args, **add_args)
    g.set(**ax_args)

    if fig_size:
        set_fig_size(g, fig_size)

    if despine:
        sns.despine(**despine)

    # tight layout
    plt.tight_layout()

    return base64img()


# -------------------------------------------------
# DISTRIBUTION PLOTS

def dis(data, x, y, hue, row, col, col_wrap, kind, rug, legend, palette, fig_size, despine={}, add_args={}, ax_args={}):

    # https://seaborn.pydata.org/generated/seaborn.displot.html#seaborn.displot

    args = clean_args(locals())

    g = sns.displot(**args, **add_args)
    g.set(**ax_args)

    if fig_size:
        set_fig_size(g, fig_size)

    if despine:
        sns.despine(**despine)

    # tight layout
    plt.tight_layout()

    return base64img()


def hist(data, x, y, hue, stat, cumulative, multiple, element, fill, shrink, kde, legend,
         palette, fig_size, despine={}, add_args={}, ax_args={}):
    # https://seaborn.pydata.org/generated/seaborn.histplot.html#seaborn.histplot

    args = clean_args(locals())

    g = sns.histplot(**args, **add_args)
    g.set(**ax_args)

    if fig_size:
        set_fig_size(g, fig_size)

    if despine:
        sns.despine(**despine)

    # tight layout
    plt.tight_layout()

    return base64img()


def kde(data, x, y, hue, cut, cumulative, multiple, common_norm, common_grid, levels, thresh,
        alpha, fill, legend, palette, fig_size, despine={}, add_args={}, ax_args={}):
    # https://seaborn.pydata.org/generated/seaborn.kdeplot.html#seaborn.kdeplot

    args = clean_args(locals())

    g = sns.kdeplot(**args, **add_args)
    g.set(**ax_args)

    if fig_size:
        set_fig_size(g, fig_size)

    if despine:
        sns.despine(**despine)

    # tight layout
    plt.tight_layout()

    return base64img()


def ecdf():
    # https://seaborn.pydata.org/generated/seaborn.ecdfplot.html#seaborn.ecdfplot
    pass


def rug():
    # https://seaborn.pydata.org/generated/seaborn.rugplot.html#seaborn.rugplot
    pass


# -------------------------------------------------
# CATEGORICAL PLOTS


def cat(data, x, y, hue, row, col, col_wrap, ci, seed, kind, palette, fig_size, despine={}, add_args={}, ax_args={}):
    # https://seaborn.pydata.org/generated/seaborn.catplot.html#seaborn.catplot

    args = clean_args(locals())

    g = sns.catplot(**args, **add_args)
    g.set(**ax_args)

    if fig_size:
        set_fig_size(g, fig_size)

    if despine:
        sns.despine(**despine)

    # tight layout
    plt.tight_layout()

    return base64img()


def strip(data, x, y, hue, jitter, size, palette, fig_size, despine={}, add_args={}, ax_args={}):
    # https://seaborn.pydata.org/generated/seaborn.stripplot.html#seaborn.stripplot

    args = clean_args(locals())

    g = sns.stripplot(**args, **add_args)
    g.set(**ax_args)

    if fig_size:
        set_fig_size(g, fig_size)

    if despine:
        sns.despine(**despine)

    # tight layout
    plt.tight_layout()

    return base64img()


def swarm(data, x, y, hue, dodge, size, palette, fig_size, despine={}, add_args={}, ax_args={}):
    # https://seaborn.pydata.org/generated/seaborn.swarmplot.html#seaborn.swarmplot

    args = clean_args(locals())

    g = sns.swarmplot(**args, **add_args)
    g.set(**ax_args)

    if fig_size:
        set_fig_size(g, fig_size)

    if despine:
        sns.despine(**despine)

    # tight layout
    plt.tight_layout()

    return base64img()


def box(data, x, y, hue, palette, fig_size, despine={}, add_args={}, ax_args={}):
    # https://seaborn.pydata.org/generated/seaborn.boxplot.html#seaborn.boxplot
    # get all local arguments and check if = ''

    args = clean_args(locals())

    g = sns.boxplot(**args, **add_args)
    g.set(**ax_args)

    if fig_size:
        set_fig_size(g, fig_size)

    if despine:
        sns.despine(**despine)

    # tight layout
    plt.tight_layout()

    return base64img()


def violin(data, x, y, hue, bw, inner, split, dodge, palette, fig_size, despine={}, add_args={}, ax_args={}):
    # https://seaborn.pydata.org/generated/seaborn.violinplot.html#seaborn.violinplot

    args = clean_args(locals())

    g = sns.violinplot(**args, **add_args)
    g.set(**ax_args)

    if fig_size:
        set_fig_size(g, fig_size)

    if despine:
        sns.despine(**despine)

    # tight layout
    plt.tight_layout()

    return base64img()


def boxen(data, x, y, hue, dodge, k_depth, showfliers, palette, fig_size, despine={}, add_args={}, ax_args={}):
    # https://seaborn.pydata.org/generated/seaborn.boxenplot.html#seaborn.boxenplot

    args = clean_args(locals())

    g = sns.boxenplot(**args, **add_args)
    g.set(**ax_args)

    if fig_size:
        set_fig_size(g, fig_size)

    if despine:
        sns.despine(**despine)

    # tight layout
    plt.tight_layout()

    return base64img()


def point(data, x, y, hue, dodge, join, scale, errwidth, palette, fig_size, despine={}, add_args={}, ax_args={}):
    # https://seaborn.pydata.org/generated/seaborn.pointplot.html#seaborn.pointplot

    args = clean_args(locals())

    g = sns.pointplot(**args, **add_args)
    g.set(**ax_args)

    if fig_size:
        set_fig_size(g, fig_size)

    if despine:
        sns.despine(**despine)

    # tight layout
    plt.tight_layout()

    return base64img()


def bar(data, x, y, hue, ci, errwidth, palette, fig_size, despine={}, add_args={}, ax_args={}):
    # https://seaborn.pydata.org/generated/seaborn.barplot.html#seaborn.barplot

    args = clean_args(locals())

    g = sns.barplot(**args, **add_args)
    g.set(**ax_args)

    if fig_size:
        set_fig_size(g, fig_size)

    if despine:
        sns.despine(**despine)

    # tight layout
    plt.tight_layout()

    return base64img()


def count(data, x, hue, dodge, palette, fig_size, despine={}, add_args={}, ax_args={}):
    # https://seaborn.pydata.org/generated/seaborn.countplot.html#seaborn.countplot

    args = clean_args(locals())

    g = sns.countplot(**args, **add_args)
    g.set(**ax_args)

    if fig_size:
        set_fig_size(g, fig_size)

    if despine:
        sns.despine(**despine)

    # tight layout
    plt.tight_layout()

    return base64img()

# -----------------------

def joint(data, x, y, hue, kind, palette, fig_size,  despine={}, add_args={}, ax_args={}):
    # https://seaborn.pydata.org/generated/seaborn.jointplot.html#seaborn.jointplot

    args = clean_args(locals())
    
    # check that x and y columns are numeric 
    if sum([check_numeric(data, x) for x in [x, y]]) != 2:
        raise ValueError(f'x column "{x}" and y columns "{y}" must be numeric')
    
    g = sns.jointplot(**args, **add_args)
    # g.set(**ax_args) # joint plot does not have an ax_args 

    if fig_size:
        set_fig_size(g, fig_size)
  
    if despine:
        sns.despine(**despine)

    # tight layout
    plt.tight_layout()

    return base64img()

# -----------------------
def pair(data, hue, vars, x_vars, y_vars, palette, kind, diag_kind, corner, fig_size, despine={}, add_args={}, ax_args={}):
    # https://seaborn.pydata.org/generated/seaborn.pairplot.html#seaborn.pairplot

    args = clean_args(locals())

    g = sns.pairplot(**args, **add_args)
    g.set(**ax_args)

    if fig_size:
        set_fig_size(g, fig_size)

    if despine:
        sns.despine(**despine)

    # tight layout
    plt.tight_layout()

    return base64img()
