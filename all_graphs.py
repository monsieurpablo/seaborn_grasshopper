import base64
from matplotlib import pyplot as plt
import seaborn as sns
import io
import os


def base64img():
    # https://stackoverflow.com/questions/37225035/serialize-in-json-a-base64-encoded-data
    my_stringIObytes = io.BytesIO()

    plt.savefig(my_stringIObytes, format='png')
    plt.close()

    my_stringIObytes.seek(0)
    imdata_bytes = base64.b64encode(my_stringIObytes.read())
    imdata_string = imdata_bytes.decode('utf-8')
    return imdata_string

def empty2none(args):
    for k, v in args.items():
        if type(v) == str:
            args[k] = None if v == '' else v
    return args

def clean_args(args):  
    # remove optional args
    args.pop('add_args')
    args.pop('ax_args')
    args.pop('despine')
    
    args = empty2none(args)
    
    return args
    

# ---------------------------------
# RELATIONAL PLOTS


def rel(data, x, y, hue, palette, despine={}, add_args={}, ax_args={}):
    # https://seaborn.pydata.org/generated/seaborn.relplot.html#seaborn.relplot
    
    args = clean_args(locals())

    g = sns.relplot(**args, **add_args)
    g.set(**ax_args)
        
    if despine:
        sns.despine(**despine)
    
    # tight layout
    plt.tight_layout()
    
    return base64img()


def scatter(data, x, y, hue, palette, despine={}, add_args={}, ax_args={}):
    # https://seaborn.pydata.org/generated/seaborn.scatterplot.html#seaborn.scatterplot
 
    args = clean_args(locals())

    g = sns.scatterplot(**args, **add_args)
    g.set(**ax_args)
        
    if despine:
        sns.despine(**despine)
    
    # tight layout
    plt.tight_layout()

    return base64img()


def line(data, x, y, hue, palette, despine={}, add_args={}, ax_args={} ):
    # https://seaborn.pydata.org/generated/seaborn.lineplot.html#seaborn.lineplot
    
    args = clean_args(locals())

    g = sns.lineplot(**args, **add_args)
    g.set(**ax_args)
        
    if despine:
        sns.despine(**despine)
    
    # tight layout
    plt.tight_layout()

    return base64img()


# -------------------------------------------------
# DISTRIBUTION PLOTS

def dis(data, x, y, hue, kind, rug, legend, palette, despine={}, add_args={}, ax_args={} ):

    # https://seaborn.pydata.org/generated/seaborn.displot.html#seaborn.displot
    
    args = clean_args(locals())

    g = sns.displot(**args, **add_args)
    g.set(**ax_args)
        
    if despine:
        sns.despine(**despine)
    
    # tight layout
    plt.tight_layout()

    return base64img()


def hist(data, x, y, hue, stat, cumulative, multiple, element, fill, shrink, kde, legend,
         palette, despine={}, add_args={}, ax_args={} ):
    # https://seaborn.pydata.org/generated/seaborn.histplot.html#seaborn.histplot

    args = clean_args(locals())

    g = sns.histplot(**args, **add_args)
    g.set(**ax_args)
        
    if despine:
        sns.despine(**despine)
    
    # tight layout
    plt.tight_layout()

    return base64img()


def kde(data, x, y, hue, cut, cumulative, multiple, common_norm, common_grid, levels, thresh,
        alpha, fill, legend, palette, despine={}, add_args={}, ax_args={} ):
    # https://seaborn.pydata.org/generated/seaborn.kdeplot.html#seaborn.kdeplot

    args = clean_args(locals())

    g = sns.kdeplot(**args, **add_args)
    g.set(**ax_args)
        
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


def cat(data, x, y, hue, ci, seed, kind, palette, despine={}, add_args={}, ax_args={} ):
    # https://seaborn.pydata.org/generated/seaborn.catplot.html#seaborn.catplot
    
    args = clean_args(locals())

    g = sns.catplot(**args, **add_args)
    g.set(**ax_args)
        
    if despine:
        sns.despine(**despine)
    
    # tight layout
    plt.tight_layout()

    return base64img()


def strip(data, x, y, hue, jitter, size, palette, despine={}, add_args={}, ax_args={}):
    # https://seaborn.pydata.org/generated/seaborn.stripplot.html#seaborn.stripplot
    
    args = clean_args(locals())

    g = sns.stripplot(**args, **add_args)
    g.set(**ax_args)
        
    if despine:
        sns.despine(**despine)
    
    # tight layout
    plt.tight_layout()
    
    return base64img()


def swarm(data, x, y, hue, dodge, size, palette, despine={}, add_args={}, ax_args={}):
    # https://seaborn.pydata.org/generated/seaborn.swarmplot.html#seaborn.swarmplot
    
    args = clean_args(locals())

    g = sns.swarmplot(**args, **add_args)
    g.set(**ax_args)
        
    if despine:
        sns.despine(**despine)
    
    # tight layout
    plt.tight_layout()

    return base64img()


def box(data, x, y, hue, palette, despine={}, add_args={}, ax_args={} ):
    # https://seaborn.pydata.org/generated/seaborn.boxplot.html#seaborn.boxplot
    # get all local arguments and check if = ''

    args = clean_args(locals())

    g = sns.boxplot(**args, **add_args)
    g.set(**ax_args)
        
    if despine:
        sns.despine(**despine)
    
    # tight layout
    plt.tight_layout()

    return base64img()


def violin(data, x, y, hue, bw, inner, split, dodge, palette, despine={}, add_args={}, ax_args={} ):
    # https://seaborn.pydata.org/generated/seaborn.violinplot.html#seaborn.violinplot
    
    args = clean_args(locals())

    g = sns.violinplot(**args, **add_args)
    g.set(**ax_args)
        
    if despine:
        sns.despine(**despine)
    
    # tight layout
    plt.tight_layout()

    return base64img()


def boxen(data, x, y, hue, dodge, k_depth, showfliers, palette, despine={}, add_args={}, ax_args={}):
    # https://seaborn.pydata.org/generated/seaborn.boxenplot.html#seaborn.boxenplot

    args = clean_args(locals())

    g = sns.boxenplot(**args, **add_args)
    g.set(**ax_args)
        
    if despine:
        sns.despine(**despine)
    
    # tight layout
    plt.tight_layout()

    return base64img()


def point(data, x, y, hue, dodge, join, scale, errwidth, palette, despine={}, add_args={}, ax_args={} ):
    # https://seaborn.pydata.org/generated/seaborn.pointplot.html#seaborn.pointplot
    
    args = clean_args(locals())

    g = sns.pointplot(**args, **add_args)
    g.set(**ax_args)
        
    if despine:
        sns.despine(**despine)
    
    # tight layout
    plt.tight_layout()

    return base64img()


def bar(data, x, y, hue, ci, errwidth, palette, despine={}, add_args={}, ax_args={} ):
    # https://seaborn.pydata.org/generated/seaborn.barplot.html#seaborn.barplot

    args = clean_args(locals())

    g = sns.barplot(**args, **add_args)
    g.set(**ax_args)
        
    if despine:
        sns.despine(**despine)
    
    # tight layout
    plt.tight_layout()

    return base64img()


def count(data, x, hue, dodge, palette, despine={}, add_args={}, ax_args={} ):
    # https://seaborn.pydata.org/generated/seaborn.countplot.html#seaborn.countplot

    args = clean_args(locals())

    g = sns.countplot(**args, **add_args)
    g.set(**ax_args)
        
    if despine:
        sns.despine(**despine)
    
    # tight layout
    plt.tight_layout()

    return base64img()

# -----------------------
