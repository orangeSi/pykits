import re
import matplotlib.pyplot as plt
import seaborn as sns

class AutoVivification(dict):
    """Implementation of perl's autovivification feature."""
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value



# change tick label size or other one times
def reset_tick_params(ax=None, ticklabel_size=8, x_labelrotation=0, y_labelrotation=0, axis="xy"):
    print (f"ticklabel_size is {ticklabel_size}")
    for i in axis.strip():
        if re.search("x", i):
            ticklables = ax.get_xticklabels()
            ax.set_xticklabels(ticklables, rotation=x_labelrotation, ha="center", va="top", fontsize=ticklabel_size )
        elif re.search("y", i):
            ticklables = ax.get_yticklabels()
            ax.set_yticklabels(ticklables, rotation=y_labelrotation, ha="right", va="center", fontsize=ticklabel_size)
        else:
            print ("error: only support x or y for axis")
            return 1
        #ax.tick_params(labelsize=ticklabel_size, axis="xy", direction="out", labelcolor,labelsize )
    #ax.tick_params(labelsize=ticklabel_size, axis=axis) will conflict with ax.set_yticklabels, so only use one!



## marker xy axis ticklabel, one group is set to  one color
def marker_ticklabel_by_sample_group(cmap="Paired",number=1000, sample_group=None, sample_order=None, ax=plt.gca(), skip_not_exists=0, axis="xy"):
    group_color = get_hex_colors_list(cmap=cmap, number=number)
    ticklabel_color = get_color_by_sample_group(sample_group=sample_group, colors=group_color, sample_order=sample_order)
    marker_color_for_ticklabel(ax=ax, colors=ticklabel_color, skip_not_exists=skip_not_exists, axis=axis)
def marker_color_for_ticklabel(ax=None, colors=None, skip_not_exists=0, axis="x"):
    t = type(colors)
    if not (t == dict or t == list):
        print ("error: marker_color_for_ticklabel not support dict or list for colors")
        return 1
    for i in axis.strip():
        if re.search("x", i):
            ticklables = ax.get_xticklabels()
        elif re.search("y", i):
            ticklables = ax.get_yticklabels()
        else:
            print ("error: only support x or y for axis")
            return 1
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
                print ("error: color dict key number is not equal to xticklabels or set skip_not_exists=1 to ignore this")
                return 1
        else:
            if len(colors) > 0:
                col = colors.pop(0)
            elif skip_not_exists:
                continue
            else:
                print ("error: color list element number is not equal to xtickalbels or set skip_not_exists=1 to ignore this")
                return 1
        l.set_color(col)
    return 0
def get_color_by_sample_group(sample_group=None, # file
                              colors=None, # list
                              sample_order=None # list
                              ):
    sample2group = {}
    group_color = {}
    with open(sample_group) as f:
        for line in f:
            line = line.strip()
            if re.match("#", line): continue
            s, g = re.split("\s+", line)
            sample2group[s] = g
            if g not in group_color:
                group_color[g] = colors.pop()
    color_order = []
    for sample in sample_order:
        col = group_color[sample2group[sample]]
        color_order.append(col)
    return color_order
def get_hex_colors_list(cmap="Paired",# Paird is from  https://seaborn.pydata.org/tutorial/color_palettes.html,  or "#9b59b6,#3498db,#e74c3c"
                        number=0 # 0 or other number.when is not 0, if the color run out, will recycle the colors. when is 0, will not recycle and get actually number of colors
                        ): # return a hex color list,
    number = int(number)
    if re.match("#", cmap): # cmap = "#9b59b6,#3498db,#e74c3c"
        colors = cmap.strip().strip(",").split(",")
    else:
        colors = sns.color_palette(cmap).as_hex()
    if number:
        while number > len(colors):
            colors = colors * 2
        colors = colors[:number]
    return colors

