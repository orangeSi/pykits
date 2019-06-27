import re
import matplotlib.pyplot as plt
import seaborn as sns
import sys

class AutoVivification(dict):
    """Implementation of perl's autovivification feature."""

    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value

def line_style(marker=[], line_styles=[], colors=[]):
    if not marker:
        markers = [".",",","o","v","^","<",">","1","2","3","4","8","s","p","P","*","h","H","+","x","X","D","d","|","_",0,1,2,3,4,5,6,7,8,9,10,11]
    if not line_styles:
        #line_styles=['-', '--', '-.', ':']
        line_styles=['-', '--', ':']
    if not colors:
        colors = ["black","green"]
    marker_style = []
    for m in markers:
        for style in line_styles:
            for c in colors:
                marker_style.append([m, style, c])
    return marker_style

def get_fsize(columns, figure_width, figure_height):
    width_ratio = 0.2
    figure_width = float(figure_width)
    figure_height = float(figure_height)
    width, height = figure_width, figure_height
    if not figure_width:
        width = width_ratio * columns
    if not figure_height:
        height = 5
    return width, height


# change tick label size or other one times


def reset_tick_params(ax=None, ticklabel_size=8, x_labelrotation=0, y_labelrotation=0, axis="xy"):
    print(f"ticklabel_size is {ticklabel_size}")
    for i in axis.strip():
        if re.search("x", i):
            ticklables = ax.get_xticklabels()
            ax.set_xticklabels(ticklables, rotation=x_labelrotation,
                               ha="center", va="top", fontsize=ticklabel_size)
        elif re.search("y", i):
            ticklables = ax.get_yticklabels()
            ax.set_yticklabels(ticklables, rotation=y_labelrotation,
                               ha="right", va="center", fontsize=ticklabel_size)
        else:
            print("error: only support x or y for axis")
            sys.exit(1)
        # ax.tick_params(labelsize=ticklabel_size, axis="xy", direction="out", labelcolor,labelsize )
    # ax.tick_params(labelsize=ticklabel_size, axis=axis) will conflict with ax.set_yticklabels, so only use one!


# marker xy axis ticklabel, one group is set to  one color
def marker_ticklabel_by_sample_group(cmap="Paired", number=1000, sample_group=None, sample_order=None, ax=None, skip_not_exists=0, axis="xy", recycle_color=True):
    group_color = get_hex_colors_list(
        cmap=cmap, number=number, recycle=recycle_color)
    ticklabel_color,legend_color_label = get_color_by_sample_group(
        sample_group=sample_group, colors=group_color, sample_order=sample_order)
    add_legend(legend_color_label, ax)
    marker_color_for_ticklabel(
        ax=ax, colors=ticklabel_color, skip_not_exists=skip_not_exists, axis=axis)


def add_legend(legend_color_label, ax):
    patches = []
    import matplotlib.patches as mpatches
    for label in legend_color_label:
        patch = mpatches.Patch(color=legend_color_label[label], label=label)
        patches.append(patch)
    plt.legend(handles=patches)

def marker_color_for_ticklabel(ax=None, colors=None, skip_not_exists=0, axis="x"):
    t = type(colors)
    if not (t == dict or t == list):
        print("error: marker_color_for_ticklabel not support dict or list for colors")
        sys.exit(1)
    for i in axis.strip():
        if re.search("x", i):
            ticklables = ax.get_xticklabels()
        elif re.search("y", i):
            ticklables = ax.get_yticklabels()
        else:
            print("error: only support x or y for axis")
            sys.exit(1)
        maker_color_ticklables(ticklables, t, colors, skip_not_exists)


def maker_color_ticklables(ticklables, t, colors, skip_not_exists):
    for l in ticklables:
        text = l.get_text()
        if t == dict:
            if text in colors:
                col = colors[text]
            elif skip_not_exists:
                continue
            else:
                print(
                    "error: color dict key number is not equal to xticklabels or set skip_not_exists=1 to ignore this")
                sys.exit(1)
        else:
            if len(colors) > 0:
                col = colors.pop(0)
            elif skip_not_exists:
                continue
            else:
                print(
                    "error: color list element number is not equal to xtickalbels or set skip_not_exists=1 to ignore this")
                sys.exit(1)
        l.set_color(col)
        #print(f"label {text}, color is {col}")
    return 0


def get_color_by_sample_group(sample_group=None,  # file
                              colors=None,  # list
                              sample_order=None,  # list
                              default_color="black"
                              ):
    sample2group = {}
    group_color = {}
    print(f"sample2group is {sample_group}, sample_order is {sample_order}")
    if sample_group:
        with open(sample_group) as f:
            for line in f:
                line = line.strip()
                if re.match("#", line):
                    continue
                s, g = re.split("\t", line)
                if s not in sample_order:
                    continue
                sample2group[s] = g
    color_order = []
    legend_color_label = dict()
    for sample in sample_order:
        if not sample_group:
            sample2group[sample] = "g"
        if sample not in sample2group or not sample_group:
            col = default_color
            #print(f"{sample} not in {sample_group}, col is {col}")
        else:
            g = sample2group[sample]
            if g not in group_color:
                col = colors.pop()
                group_color[g] = col
            else:
                col = group_color[g]
            legend_color_label[g] = group_color[g]
            # print(f"{sample}->{sample2group[sample]}->{col}")
            #print(f"{sample} in {sample_group}, col is {col}")
        color_order.append(col)
    #print(f"color_order is {color_order}")
    return color_order, legend_color_label


def get_hex_colors_list(cmap="Paired",  # Paird is from  https://seaborn.pydata.org/tutorial/color_palettes.html,  or "#9b59b6,#3498db,#e74c3c"
                        number=1,
                        recycle=False,  # if  the color run out, will recycle the colors. when is 0, will not recycle and get actually number of colors
                        ):  # return a hex color list,
    number = int(number)
    print(f"cmap is {cmap}")
    if re.match("#", cmap):  # cmap = "#9b59b6,#3498db,#e74c3c"
        colors = cmap.strip().strip(",").split(",")
    elif re.search(",", cmap):
        colors = cmap.split(',')
    else:
        colors = sns.color_palette(cmap).as_hex()
    if recycle:
        while number > len(colors):
            colors = colors * 2
        colors = colors[:number]
    else:
        if number > len(colors):
            sys.exit(
                print("error:number={number}, but only get {len(colors)} colors:{colors}"))
    return colors
