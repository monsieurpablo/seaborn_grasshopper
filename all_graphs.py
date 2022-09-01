from matplotlib import pyplot as plt
import seaborn as sns


# ---------------------------------
# RELATIONAL PLOTS


def rel(g_dt, g_x_ax, g_y_ax, g_hue, g_palette):
    # https://seaborn.pydata.org/generated/seaborn.relplot.html#seaborn.relplot
    if g_hue == '':
        sns.relplot(
            data=g_dt,
            x=g_x_ax,
            y=g_y_ax,
            palette=g_palette
        )
    else:
        sns.relplot(
            data=g_dt,
            x=g_x_ax,
            y=g_y_ax,
            hue=g_hue,
            palette=g_palette
        )
    plt.show()
    plt.close()


def no_default(g_dt, g_x_ax, g_y_ax, g_palette, g_hue):
    # https://seaborn.pydata.org/generated/seaborn.relplot.html#seaborn.relplot

    sns.relplot(
        data=g_dt,
        x=g_x_ax,
        y=g_y_ax,
        hue=g_hue,
        palette=g_palette
    )

    plt.show()
    plt.close()


def scatter(g_dt, g_x_ax, g_y_ax, g_hue, g_palette):
    # https://seaborn.pydata.org/generated/seaborn.scatterplot.html#seaborn.scatterplot
    if g_hue == '':
        sns.scatterplot(
            data=g_dt,
            x=g_x_ax,
            y=g_y_ax,
            palette=g_palette
        )
    else:
        sns.scatterplot(
            data=g_dt,
            x=g_x_ax,
            y=g_y_ax,
            hue=g_hue,
            palette=g_palette
        )
    plt.show()
    plt.close()


def line(g_dt, g_x_ax, g_y_ax, g_hue, g_palette):
    # https://seaborn.pydata.org/generated/seaborn.lineplot.html#seaborn.lineplot
    if g_hue == '':
        sns.lineplot(
            data=g_dt,
            x=g_x_ax,
            y=g_y_ax,
            palette=g_palette
        )
    else:
        sns.lineplot(
            data=g_dt,
            x=g_x_ax,
            y=g_y_ax,
            hue=g_hue,
            palette=g_palette
        )
    plt.show()
    plt.close()


# -------------------------------------------------
# DISTRIBUTION PLOTS

def dis(g_dt, g_x_ax, g_y_ax, g_hue, g_kind, g_rug, g_legend, g_palette):
    if g_hue == '':
        if g_y_ax == '':
            sns.displot(
                data=g_dt,
                x=g_x_ax,
                kind=g_kind,
                rug=g_rug,
                legend=g_legend,
                palette=g_palette
            )
        else:
            sns.displot(
                data=g_dt,
                x=g_x_ax,
                y=g_y_ax,
                kind=g_kind,
                rug=g_rug,
                legend=g_legend,
                palette=g_palette
            )
    else:
        if g_y_ax == '':
            sns.displot(
                data=g_dt,
                x=g_x_ax,
                hue=g_hue,
                kind=g_kind,
                rug=g_rug,
                legend=g_legend,
                palette=g_palette
            )
        else:
            sns.displot(
                data=g_dt,
                x=g_x_ax,
                y=g_y_ax,
                hue=g_hue,
                kind=g_kind,
                rug=g_rug,
                legend=g_legend,
                palette=g_palette
            )
    plt.show()
    plt.close()


def hist(g_dt, g_x_ax, g_y_ax, g_hue, g_stat, g_cumulative, g_multiple, g_element, g_fill, g_shrink, g_kde, g_legend,
         g_palette):
    # https://seaborn.pydata.org/generated/seaborn.histplot.html#seaborn.histplot
    if g_hue == '':
        if g_y_ax == '':
            sns.histplot(
                data=g_dt,
                x=g_x_ax,
                stat=g_stat,
                cumulative=g_cumulative,
                multiple=g_multiple,
                element=g_element,
                fill=g_fill,
                shrink=g_shrink,
                kde=g_kde,
                legend=g_legend,
                palette=g_palette
            )
        else:
            sns.histplot(
                data=g_dt,
                x=g_x_ax,
                y=g_y_ax,
                stat=g_stat,
                cumulative=g_cumulative,
                multiple=g_multiple,
                element=g_element,
                fill=g_fill,
                shrink=g_shrink,
                kde=g_kde,
                legend=g_legend,
                palette=g_palette
            )
    else:
        if g_y_ax == '':
            sns.histplot(
                data=g_dt,
                x=g_x_ax,
                hue=g_hue,
                stat=g_stat,
                cumulative=g_cumulative,
                multiple=g_multiple,
                element=g_element,
                fill=g_fill,
                shrink=g_shrink,
                kde=g_kde,
                legend=g_legend,
                palette=g_palette
            )
        else:
            sns.histplot(
                data=g_dt,
                x=g_x_ax,
                y=g_y_ax,
                hue=g_hue,
                stat=g_stat,
                cumulative=g_cumulative,
                multiple=g_multiple,
                element=g_element,
                fill=g_fill,
                shrink=g_shrink,
                kde=g_kde,
                legend=g_legend,
                palette=g_palette
            )
    plt.show()
    plt.close()


def kde(g_dt, g_x_ax, g_y_ax, g_hue, g_cut, g_cumulative, g_multiple, g_common_norm, g_common_grid, g_levels, g_thresh,
        g_alpha, g_fill, g_legend, g_palette):
    # https://seaborn.pydata.org/generated/seaborn.kdeplot.html#seaborn.kdeplot
    if g_hue == '':
        if g_y_ax == '':
            sns.kdeplot(
                data=g_dt,
                x=g_x_ax,
                cut=g_cut,
                cumulative=g_cumulative,
                multiple=g_multiple,
                common_norm=g_common_norm,
                common_grid=g_common_grid,
                levels=g_levels,
                thresh=g_thresh,
                alpha=g_alpha,
                fill=g_fill,
                legend=g_legend,
                palette=g_palette
            )
        else:
            sns.kdeplot(
                data=g_dt,
                x=g_x_ax,
                y=g_y_ax,
                cut=g_cut,
                cumulative=g_cumulative,
                multiple=g_multiple,
                common_norm=g_common_norm,
                common_grid=g_common_grid,
                levels=g_levels,
                thresh=g_thresh,
                alpha=g_alpha,
                fill=g_fill,
                legend=g_legend,
                palette=g_palette
            )
    else:
        if g_y_ax == '':
            sns.kdeplot(
                data=g_dt,
                x=g_x_ax,
                hue=g_hue,
                cut=g_cut,
                cumulative=g_cumulative,
                multiple=g_multiple,
                common_norm=g_common_norm,
                common_grid=g_common_grid,
                levels=g_levels,
                thresh=g_thresh,
                alpha=g_alpha,
                fill=g_fill,
                legend=g_legend,
                palette=g_palette
            )
        else:
            sns.kdeplot(
                data=g_dt,
                x=g_x_ax,
                y=g_y_ax,
                hue=g_hue,
                cut=g_cut,
                cumulative=g_cumulative,
                multiple=g_multiple,
                common_norm=g_common_norm,
                common_grid=g_common_grid,
                levels=g_levels,
                thresh=g_thresh,
                alpha=g_alpha,
                fill=g_fill,
                legend=g_legend,
                palette=g_palette
            )
    plt.show()
    plt.close()


def ecdf():
    # https://seaborn.pydata.org/generated/seaborn.ecdfplot.html#seaborn.ecdfplot
    pass


def rug():
    # https://seaborn.pydata.org/generated/seaborn.rugplot.html#seaborn.rugplot
    pass


# -------------------------------------------------
# CATEGORICAL PLOTS


def cat(g_dt, g_x_ax, g_y_ax, g_hue, g_ci, g_seed, g_kind, g_palette):
    # https://seaborn.pydata.org/generated/seaborn.catplot.html#seaborn.catplot
    if g_hue == '':
        sns.catplot(
            data=g_dt,
            x=g_x_ax,
            y=g_y_ax,
            ci=g_ci,
            seed=g_seed,
            kind=g_kind,
            palette=g_palette
        )
    else:
        sns.catplot(
            data=g_dt,
            x=g_x_ax,
            y=g_y_ax,
            hue=g_hue,
            ci=g_ci,
            seed=g_seed,
            kind=g_kind,
            palette=g_palette
        )
    plt.show()
    plt.close()


def strip(g_dt, g_x_ax, g_y_ax, g_hue, g_jitter, g_palette, g_size):
    # https://seaborn.pydata.org/generated/seaborn.stripplot.html#seaborn.stripplot
    if g_hue == '':
        sns.stripplot(
            data=g_dt,
            x=g_x_ax,
            y=g_y_ax,
            jitter=g_jitter,
            palette=g_palette,
            size=g_size
        )
    else:
        sns.stripplot(
            data=g_dt,
            x=g_x_ax,
            y=g_y_ax,
            hue=g_hue,
            jitter=g_jitter,
            palette=g_palette,
            size=g_size
        )
    plt.show()
    plt.close()


def swarm(g_dt, g_x_ax, g_y_ax, g_hue, g_dodge, g_palette, g_size):
    # https://seaborn.pydata.org/generated/seaborn.swarmplot.html#seaborn.swarmplot
    if g_hue == '':
        sns.swarmplot(
            data=g_dt,
            x=g_x_ax,
            y=g_y_ax,
            dodge=g_dodge,
            palette=g_palette,
            size=g_size
        )
    else:
        sns.swarmplot(
            data=g_dt,
            x=g_x_ax,
            y=g_y_ax,
            hue=g_hue,
            dodge=g_dodge,
            palette=g_palette,
            size=g_size
        )
    plt.show()
    plt.close()


def box(g_dt, g_x_ax, g_y_ax, g_hue, g_palette):
    # https://seaborn.pydata.org/generated/seaborn.boxplot.html#seaborn.boxplot
    if g_hue == '':
        sns.boxplot(
            data=g_dt,
            x=g_x_ax,
            y=g_y_ax,
            palette=g_palette,
        )
    else:
        sns.boxplot(
            data=g_dt,
            x=g_x_ax,
            y=g_y_ax,
            hue=g_hue,
            palette=g_palette,
        )
    plt.show()
    plt.close()


def violin(g_dt, g_x_ax, g_y_ax, g_hue, g_bw, g_inner, g_split, g_dodge, g_palette):
    # https://seaborn.pydata.org/generated/seaborn.violinplot.html#seaborn.violinplot
    if g_hue == '':
        sns.violinplot(
            data=g_dt,
            x=g_x_ax,
            y=g_y_ax,
            bw=g_bw,
            inner=g_inner,
            split=g_split,
            dodge=g_dodge,
            palette=g_palette,
        )
    else:
        sns.violinplot(
            data=g_dt,
            x=g_x_ax,
            y=g_y_ax,
            hue=g_hue,
            bw=g_bw,
            inner=g_inner,
            split=g_split,
            dodge=g_dodge,
            palette=g_palette,
        )
    plt.show()
    plt.close()


def boxen(g_dt, g_x_ax, g_y_ax, g_hue, g_dodge, g_k_depth, g_palette, g_showfliers):
    # https://seaborn.pydata.org/generated/seaborn.boxenplot.html#seaborn.boxenplot
    if g_hue == '':
        sns.boxenplot(
            data=g_dt,
            x=g_x_ax,
            y=g_y_ax,
            dodge=g_dodge,
            k_depth=g_k_depth,
            palette=g_palette,
            showfliers=g_showfliers
        )
    else:
        sns.boxenplot(
            data=g_dt,
            x=g_x_ax,
            y=g_y_ax,
            hue=g_hue,
            dodge=g_dodge,
            k_depth=g_k_depth,
            palette=g_palette,
            showfliers=g_showfliers
        )
    plt.show()
    plt.close()


def point(g_dt, g_x_ax, g_y_ax, g_hue, g_dodge, g_join, g_scale, g_errwidth, g_palette):
    # https://seaborn.pydata.org/generated/seaborn.pointplot.html#seaborn.pointplot
    if g_hue == '':
        sns.pointplot(
            data=g_dt,
            x=g_x_ax,
            y=g_y_ax,
            dodge=g_dodge,
            join=g_join,
            scale=g_scale,
            errwidth=g_errwidth,
            palette=g_palette
        )
    else:
        sns.pointplot(
            data=g_dt,
            x=g_x_ax,
            y=g_y_ax,
            hue=g_hue,
            dodge=g_dodge,
            join=g_join,
            scale=g_scale,
            errwidth=g_errwidth,
            palette=g_palette
        )
    plt.show()
    plt.close()


def bar(g_dt, g_x_ax, g_y_ax, g_hue, g_ci, g_errwidth, g_palette):
    # https://seaborn.pydata.org/generated/seaborn.barplot.html#seaborn.barplot
    if g_hue == '':
        sns.barplot(
            data=g_dt,
            x=g_x_ax,
            y=g_y_ax,
            ci=g_ci,
            errwidth=g_errwidth,
            palette=g_palette
        )
    else:
        sns.barplot(
            data=g_dt,
            x=g_x_ax,
            y=g_y_ax,
            hue=g_hue,
            ci=g_ci,
            errwidth=g_errwidth,
            palette=g_palette
        )
    plt.show()
    plt.close()


def count(g_dt, g_x_ax, g_hue, g_dodge, g_palette):
    # https://seaborn.pydata.org/generated/seaborn.countplot.html#seaborn.countplot
    if g_hue == '':
        sns.countplot(
            data=g_dt,
            x=g_x_ax,
            dodge=g_dodge,
            palette=g_palette
        )
    else:
        sns.countplot(
            data=g_dt,
            x=g_x_ax,
            hue=g_hue,
            dodge=g_dodge,
            palette=g_palette
        )
    plt.show()
    plt.close()

# -----------------------
