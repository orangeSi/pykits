#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
import matplotlib as mpl
mpl.use('Agg')
import baselib.plot_core as bpc
import fire_table
import datetime
import fire
import re
import os
import sys
import pyvenn_modify.venn as venn
import palettable
import pandas as pd
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.gridspec as gridspec
import seaborn as sns
print("start import lib, you have a break time for few seconds now")
# import matplotlib
# Force matplotlib to not use any Xwindows backend.

# my libs

print("end import lib")

# def show_time():
#    return datetime.datetime.now()


def show_time(func):
    def wrapper(*args, **kwargs):
        datetime.datetime.now()
        return func(*args, **kwargs)
    return wrapper

# @show_time


class sns_ploter():
    def __init__(self, same_outdir=0, outdir=".", prefix="test", data="", oformats="pdf,png", header=0, index_col=0, sep="\t", dpi=300):
        """
        usage:
            python /ifswh1/BC_PS/sikaiwei/bin/python3/lib/fire.sns.py clustermap --data dataframe.xls  --header 0 --index-col 0 --linewidths 0.2 --outdir . --prefix Class.all.heatmap.new --oformat pdf

        python /ifswh1/BC_PS/sikaiwei/bin/python3/lib/fire.sns.py heatmap    --data dataframe.xls  --header 0 --index-col 0 --linewidths 0.2 --outdir . --prefix Phylum.gt1percent.kruskal.test.txt.heatmap --oformat pdf --order_x "LP.0d,LP.L.7d,LP.L.14d,LP.S.7d,LP.S.14d,OJ.0d,OJ.L.7d,OJ.L.14d,OJ.S.7d,OJ.S.14d" --order_y "Bacteroidetes,Proteobacteria"

        python /ifswh1/BC_PS/sikaiwei/bin/python3/lib/fire.sns.py heatmap-homemade --data Class.gt1.kruskal.test.txt.new2 --header 0 --index-col 0 --linewidths 0.2 --outdir . --prefix Class.gt1.kruskal.test.txt.new2.heatmap --oformat pdf --order_x LP.0d,LP.L.7d,LP.L.14d,LP.S.7d,LP.S.14d,OJ.0d,OJ.L.7d,OJ.L.14d,OJ.S.7d,OJ.S.14d --xlabel-rotation 90 --ylabel-rotation 0 --legend-ncol 1 --color-segments '#FAEBD7,#FFEBCD,#F5DEB3,#8B4513' --value_segments 0.5:1,1:2,2:5,5:15

        python  fire_sns.py  barplot --same_outdir 1 --prefix  xx --data Species.all_relative_abundance.xls --oformats "pdf,png" barplot --fig-width 35 --fig-height 10 --legend-locus bottom --ncol-leg 5  --marker-key Lactobacillus

        python  fire_sns.py  barplot --outdir . --prefix  xx --data Species.all_relative_abundance.xls --oformats "pdf,png" barplot --fig-width 35 --fig-height 10 --legend-locus bottom --ncol-leg 0

        python  fire_sns.py  barplot --outdir . --prefix  xx --data Species.all_relative_abundance.xls --oformats "pdf,png" barplot --fig_width_scale 0.35 --fig-height 10 --legend-locus bottom --ncol-leg 0

        python  fire_sns.py  --dpi 600 --data OTU_shared_for_alpha_diversity.xls.new venn --title High.intensity.pre,High.intensity.intra,High.intensity.post --sample2group s2g --title_type group
        python  fire_sns.py --data $data --prefix $data  line_yscale  --cutoff $cutoff --width_ratios 1,1 --height_ratios 1,2 --scale_axis 'y' --figure_width 16 --figure_height 6

        """
        if int(same_outdir):
            outdir = data+"."
        else:
            outdir = outdir+"/"
            self.data = data
            self.outfile = []
            self.header = int(header)
            self.index_col = int(index_col)
            self.sep = str(sep)
            self.dpi = int(dpi)
            oformats = fire_table.tablet().parse_tuple(oformats)
            if re.search(",", oformats):
                oformats = oformats.strip(",").strip().split(",")
                for oformat in oformats:
                    self.outfile.append(outdir+prefix+"."+oformat)
                print(self.outfile)

    def venn(self, sample2group="", title="",  # --title A,B,C or list for api
             title_type="sample",  # sample or group
             sets=None,  # list
             limit=0,
             fontsize=15):  # turnover=0
        fontsize = int(fontsize)
        title = fire_table.tablet().parse_tuple(title)
        title_list = re.findall(',', title)
        title_num = len(title_list)
        if title_num == 0:
            print(
                f"error: --title {title} should contain , like --title A,B,C")
            sys.exit(1)
        elif title_num >= 7:
            print(
                f"error: --title {title} should contain {title_num}, but should <= 6")
            sys.exit(1)
        if title_type != "sample" and title_type != "group":
            print(f"error: --title_type {title_type}, only support sample or group")
            sys.exit(1)
        titles = title.strip().split(",")
        venn_sets = {}
        if not sets:
            df = pd.read_csv(self.data, header=self.header,
                                     index_col=self.index_col, sep=self.sep)
                    # if int(turnover): df = df.T
            if title_type == "sample":
                        title_index = (set(df.index).intersection(
                            set(titles)) == set(titles))
                        title_column = (set(df.columns).intersection(
                            set(titles)) == set(titles))
                        if title_index and title_column:
                            print(
                                f"error, --data {sefl.data} row and column both have --title")
                            sys.exit(1)
                        elif not title_index and not title_column:
                            print(
                                f"error: --data {self.data} not contain --title {title}")
                            sys.exit(1)
                            if title_index:
                                for t in titles:
                                    venn_sets[t] = list(
                                        df.loc[t][df.loc[t] > int(limit)].to_frame().index)
                                    print(
                                        f"sample {t} have {len(venn_sets[t])} elements")
                            else:
                                for t in titles:
                                    venn_sets[t] = list(
                                        df[t][df[t] > int(limit)].to_frame().index)
                                    print(
                                        f"sample {t} have {len(venn_sets[t])} elements")
                        else:  # group
                            if not sample2group:
                                print(
                                    f"error: --sample2group {sample2group} file not exists")
                                sys.exit(1)
                                s2g = self.parse_A2B(sample2group, 0, 1)
                                all_sample = [
                                    s for s in s2g if s2g[s] in titles]
                                gs = list(set([s2g[s] for s in s2g]))
                                for i in titles:
                                    if i not in gs:
                                        print(
                                            f"error:group {i} not in --sample2group {sample2group}")
                                        sys.exit(1)
                                        title_index = (set(df.index).intersection(
                                            set(all_sample)) == set(all_sample))
                                        title_column = (set(df.columns).intersection(
                                            set(all_sample)) == set(all_sample))
                                        if title_index and title_column:
                                            print(
                                                f"error, --data {sefl.data} row and column both have --title")
                                            sys.exit(1)
                                        elif not title_index and not title_column:
                                            print(
                                                f"error: --data {self.data} not contain --title {title}")
                                            sys.exit(1)
                                            venn_sets[i] = venn_sets.get(i, [])
                                            ss = list(
                                                set([s for s in s2g if s2g[s] == i]))
                                            print(f"group {i} -> {ss}")
                                            for s in ss:
                                                if title_index:
                                                    venn_sets[i] += list(
                                                        df.loc[s][df.loc[s] > int(limit)].to_frame().index)
                                                else:
                                                    venn_sets[i] += list(
                                                        df[s][df[s] > int(limit)].to_frame().index)
                                                    venn_sets[i] = list(
                                                        set(venn_sets[i]))
                                                    print(
                                                        f"group {i} have {len(venn_sets[i])} elements")
                                                    # get venn_sets[key] = [elemses]
                                                    labels = venn.get_labels(
                                                        [venn_sets[t] for t in titles], fill=['number'])
                                        else:
                                            if type(title) != list or type(sets) != list:
                                                print(
                                                    "error: --title or --sets need to be list")
                                                sys.exit(1)
                                                if len(sets) != len(title):
                                                    print(
                                                        f"error: --sets and --title both be list and same length")
                                                    sys.exit(1)
                                                    labels = venn.get_labels(
                                                        sets, fill=['number'])
                                                    if len(titles) == 2:
                                                        fig, ax = venn.venn2(
                                                            labels, names=titles, fontsize=fontsize)
                                                    elif len(titles) == 3:
                                                        fig, ax = venn.venn3(
                                                            labels, names=titles, fontsize=fontsize)
                                                    elif len(titles) == 4:
                                                        fig, ax = venn.venn4(
                                                            labels, names=titles, fontsize=fontsize)
                                                    elif len(titles) == 5:
                                                        fig, ax = venn.venn5(
                                                            labels, names=titles, fontsize=fontsize)
                                                    elif len(titles) == 6:
                                                        fig, ax = venn.venn6(
                                                            labels, names=titles, fontsize=fontsize)
                                                        plt.tight_layout()
                                                        box = ax.get_position()
                                                        margin = 0.2
                                                        ax.set_position(
                                                            [box.x0*(1+margin), box.y0, box.width-box.x0*margin, box.height])
                                                        # plt.subplots_adjust(left=0.1)
                                                        for out in self.outfile:
                                                            plt.savefig(
                                                                out, dpi=self.dpi)
                                                            print(out)

    def parse_A2B(self, sample2group, A_column, B_column):
        A2B = {}
        if os.path.exists(sample2group):
            with open(sample2group) as f:
                for line in f:
                    line = line.strip()
                    if re.match("#", line):
                        continue
                    arr = re.split("\s+", line)
                    A2B[arr[A_column]] = arr[B_column]
        else:
            print(f"error: --sample2group {sample2group} not exists ")
            sys.exit(1)
            return A2B

    def heatmap(self, header=0, index_col=0, sep="\t", linewidths=0, dpi=200, oformat="pdf",
                cmap="coolwarm",  # coolwarm or vlag
                tick_group_color="#9b59b6,#3498db",  # "#9b59b6,#3498db, or Paired
                order_x="",
                order_y="",
                sample2group='',
                ticklabel_size=6,
                annot=0,
                y_labelrotation=0,
                x_labelrotation=70):
        if not os.path.exists(sample2group):
            print("error: need to set --sample2group")
            sys.exit(1)
            annot = int(annot)
            if annot:
                annot = True
            else:
                annot = False
                linewidths = float(linewidths)
                ticklabel_size = int(ticklabel_size)
                y_labelrotation = float(y_labelrotation)
                x_labelrotation = float(x_labelrotation)
                df = pd.read_csv(self.data, header=header,
                                 index_col=index_col, sep=sep)
                # flatui = ["#9b59b6", "#3498db", "#e74c3c", "#34495e", "#2ecc71"]
                # cmap = sns.color_palette(flatui)
                # order_x = "LP.0d,LP.L.7d,LP.L.14d,LP.S.7d,LP.S.14d,OJ.0d,OJ.L.7d,OJ.L.14d,OJ.S.7d,OJ.S.14d"
                if order_x:
                    if type(order_x) is tuple:
                        order_x = ",".join(order_x)
                    print(order_x)
                    order_x = order_x.strip().strip(",").split(",")
                    df = df[order_x]
                if order_y:
                    if type(order_y) is tuple:
                        order_y = ",".join(order_y)
                    print(order_y)
                    order_y = order_y.strip().strip(",").split(",")
                    df = df.loc[order_y, :]
                    ax = plt.gca()
                    print(f"cmap is {cmap}")
                    sns.heatmap(df, cmap=cmap, linewidths=linewidths,
                                    xticklabels=1, yticklabels=1, ax=ax, annot=annot)
                    bpc.marker_ticklabel_by_sample_group(cmap=tick_group_color, number=1000, sample_group=sample2group,
                                                             sample_order=list(df.columns)+list(df.index), ax=ax, skip_not_exists=0, axis="xy", recycle_color=1)
                    bpc.reset_tick_params(ax=ax, ticklabel_size=ticklabel_size,
                                              x_labelrotation=x_labelrotation, y_labelrotation=y_labelrotation, axis="xy")
        plt.tight_layout()
        for out in self.outfile:
            plt.savefig(out, dpi=dpi)
            print(out)

    def extract(self, data=None, data_header_contain_comment=None, keywords=None, keywords_file=None, sample2group=None, extract_index=0, extract_column=1,
                sample2group_fileds="0,1", keywords_file_field=0, header=0, index_col=0, sep="\t", comment="#",
                prefix="test.extract", same_outdir=0, outdir=".", keep_metadata=1, skip_not_exists=0, order_x=None, order_y=None,
                return_data_frame=0):
        self.dataf = fire_table.tablet().extract(data, data_header_contain_comment,
                                                 return_data_frame=1)  # fix this #sikaiwei

    def get_dataframe(self, header, index_col, sep):
        df = pd.DataFrame()
        if hasattr(self, 'dataf'):
            df = self.dataf
        else:
            df = pd.read_csv(self.data, header=header,
                             index_col=index_col, sep=sep)
            return df

    def barplot(self, fig_width=None, fig_height=10, legend_locus="bottom",  # bottom or right or auto
                ncol_leg=0,  # set ncol_leg to 0 will auto caculate the ncol, otherwise will set ncol to ncol_leg
                marker_key=None,  # marker legned
                cmap="Paired",  # for sns.color_palette("Paired") #or tab10
                # like Paired,tab10,Set2,cubehelix # for more color, go to https://seaborn.pydata.org/tutorial/color_palettes.html
                xlabel_rotation=45,
                # set fig_width=35 for x tick label number=100, so fig_width_scale=3.5
                fig_width_scale=0.35,
                turnover=True,  # add df.T or not for df , index of df of data will be the x axis
                marker_density=3,  # bigger , smaller size marker, more marker number
                ylabel="Relative abundance(%)",
                sep="\t",
                header=0,
                index_col=0,
                reuse_markers=0,
                marker_start_pos=6,
                sample2group="",
                tick_group_color="#9b59b6,#3498db"  # or Paired
                ):
        reuse_markers = int(reuse_markers)
        marker_start_pos = int(marker_start_pos)
        df = self.get_dataframe(header=header, index_col=index_col, sep=sep)
        if turnover:
            df = df.T
        mpl.rcParams['hatch.linewidth'] = 0.8  # previ
        mpl.rcParams['hatch.color'] = '#363636'  # previ
        mpl.rcParams["legend.handleheight"] = 1.4  # default 0.7
        # legend_locus = "bottom" # bottom or right
        # marker_key = "Lactobacillus"

        df = pd.read_csv(self.data, header=0, index_col=0, sep="\t")
        if turnover:
            df = df.T

        fig_w, fig_h = fig_width, fig_height
        if not fig_width:
            fig_w = float(fig_width_scale) * len(df.index)
            ncol = 1
            print(f"legend_locus is {legend_locus}")
            if legend_locus == "auto":
                pass  # continue sikaiwei
        if legend_locus == "right":
            # figure height size = 4 ->equal -> 14 pieces of legend label, when mpl.rcParams["legend.handleheight"] = 1.4
            len_ratio = 3/12
            # print (len(df.columns)*len_ratio)
            if len(df.columns)*len_ratio % fig_h > 0:
                ncol = len(df.columns)*len_ratio // fig_h + 1
            else:
                ncol = len(df.columns)*len_ratio // fig_h
                loc_leg = 'center left'
                bbox_to_anchor = (1, 0.5)
                lens = [len(i) for i in df.columns]
                columns_avg_len = float(sum(lens)) / max(len(lens), 1)
                fig_w += ncol * columns_avg_len * (4.5/25)
                # print(f"columns_avg_len is {columns_avg_len}")
        elif legend_locus == "bottom":
            loc_leg = "upper center"
            bbox_to_anchor = (0.5, -0.1)
            # one column of legend is equal to -> 10 samples width in x axis
            number_one_col = int(len(df.index)/(10*fig_width_scale/0.35))
            ncol = number_one_col
        else:
            print(f"error: not support {legend_locus} for --legend_locus yet~")
            sys.exit(1)

        print(f"{fig_w} {fig_h}")
        plt.figure(figsize=(fig_w, fig_h))
        ncol = int(ncol)
        if int(ncol_leg):
            ncol = int(ncol_leg)
        if ncol == 0:
            ncol = 1
        print(f"ncol is {ncol}")
        color_list = sns.color_palette(cmap).as_hex()
        print(f"raw color is{color_list}")
        ax = plt.gca()
        df.plot(kind='bar', stacked=True, ax=ax,
                legend=False,  color=color_list, width=0.8)
        # ax.set_xticklabels(ax.get_xlabel(), rotation = 45, ha="right")
        plt.xticks(rotation=int(xlabel_rotation), ha="center", va="top")
        # plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5), ncol=ncol)

        # leg.legendHandles[0].set_color('black')
        # leg.legendHandles[1].set_color('yellow')
        # ax = plt.gca()
        # pos = df.index.get_loc("104VB")
        # ax.patches[pos].set_facecolor('red')
        # ax.patches[pos].set_hatch("*")
        # ax.patches[0].set_facecolor('green')
        # ax.patches[2].set_facecolor('blue')
        # ax.patches[3].set_facecolor('black')

        marker_list = []
        # marker_hatch_all = ['', '.', '+', '-', 'o', '*', '/', '|', '\\', '0', 'x']
        marker_hatch_all = ['', '.', '+', '-', 'o', '*',
                            '/', '|', '\\', 'x', '.+', 'o/', 'o\\', '*+']
        # for not marker data, first 6 marker is for this
        marker_hatch_list1 = marker_hatch_all[:marker_start_pos]
        # for marker data, from 6 to last is for this
        marker_hatch_list2 = marker_hatch_all[marker_start_pos:]
        if marker_key:
            marker_list = [i for i in df.columns if re.search(marker_key, i)]
        else:
            marker_hatch_list1 = marker_hatch_all
            marker_hatch_list2 = [""]

        marker_hatch_list1 = [i * marker_density for i in marker_hatch_list1]
        marker_hatch_list2 = [i * marker_density for i in marker_hatch_list2]
        # hatch: ['/' | '\\' | '|' | '-' | '+' | 'x' | 'o' | 'O' | '.' | '*']

        # marker_fc = "orange"
        index_num = len(df.index)
        test = 0
        for i in range(index_num):  # index is sample list if turnover
            hatch_list1 = marker_hatch_list1.copy()
            hatch_list2 = marker_hatch_list2.copy()
            hatch1 = hatch_list1.pop(0)
            hatch2 = hatch_list2.pop(0)
            fc_list1 = []
            fc_list2 = []
            test += 1
            # print (f"hatch_list1 is {hatch_list1}")
            for j in df.columns:  # df.columns is species list if turnover
                pos = df.columns.get_loc(j) * index_num + i
                if len(hatch_list1) == 0:
                    hatch_list1 = marker_hatch_list1.copy()
                    # ax.patches[pos].set_edgecolor(hatch_color.pop(0))
                    # ax.patches[pos].set_linewidth(0)
                    # mpl.rcParams["hatch.color"] = hatch_color.pop(0) ## just global varaiable , not work for rest
                    # mpl.rcParams["hatch.linewidth"] += 0.2 ## just global varaiable , not work for rest
                    # print (f"hatch.color is {mpl.rcParams['hatch.color']}")
                if len(hatch_list2) == 0:
                        hatch_list2 = marker_hatch_list2.copy()
                        # ax.patches[pos].set_edgecolor(hatch_color.pop(0))
                        # ax.patches[pos].set_linewidth(0)
                if (len(hatch_list1) == 0 or len(hatch_list2) == 0) and not reuse_markers:
                        print(
                                f"error: you have used all markers. But if you want to reuse markers, set --reuse_markers to 1 ")
                        sys.exit(1)
                            # mpl.rcParams["hatch.color"] = hatch_color.pop(0) # just global varaiable , not work for rest
                            # mpl.rcParams["hatch.linewidth"] += 0.2 # just global varaiable , not work for rest
                            # print (f"hatch.color is {mpl.rcParams['hatch.color']}")
                            # if mpl.rcParams["hatch.linewidth"] >1.6 : mpl.rcParams["hatch.linewidth"] = 1.6 # just global varaiable , not work for rest

                fc = ax.patches[pos].get_facecolor()
                fc = [str(k) for k in fc]
                hatch = ''

                '''
                add hatch for every cell
                '''
                if j in marker_list:
                    fc_new = "".join(fc) + "->" + hatch2
                    if fc_new in fc_list2:
                        hatch2 = hatch_list2.pop(0)
                        fc_new = "".join(fc) + "->" + hatch2
                    if fc_new in fc_list2 and reuse_markers <= 0:
                            print(
                                f"error: you have used all markers with color. try give more colors or markers. But if you want to reuse markers, set --reuse_markers to 1 ")
                            sys.exit(1)
                            fc_list2.append(fc_new)
                            hatch = hatch2
                            # if test == 1: print (f"fc1 is {fc}, j is {j}, hatch2 is {hatch2}, fc_list2 {fc_list2}, hatch_list2 is {hatch_list2}")
                    else:
                        fc_new = "".join(fc) + "->" + hatch1
                            # if test == 1: print (f"fc3 is {fc_new}, j is {j}, hatch1 is {hatch1}, fc_list1 {fc_list1}, hatch_list1 is {hatch_list1}")
                        if fc_new in fc_list1:
                            hatch1 = hatch_list1.pop(0)
                            fc_new = "".join(fc) + "->" + hatch1
                        if fc_new in fc_list1 and reuse_markers <= 0:
                            print(f"error: you have used all markers with color. try give more colors or markers. But if you want to reuse markers, set --reuse_markers to 1 ")
                            sys.exit(1)
                                    # if test == 1: print (f"fc1 is {fc_new}, j is {j}, hatch1 is {hatch1}, fc_list1 {fc_list1}, hatch_list1 is {hatch_list1}")
                        fc_list1.append(fc_new)
                                    # print(f"fc_new is {fc_new}")
                                    # ddif test == 1: print (f"fc2 is {fc_new}, j is {j}, hatch1 is {hatch1}, fc_list1 {fc_list1}, hatch_list1 is {hatch_list1}")
                        hatch = hatch1
                                    # print(f"hatch is {hatch}")
                        ax.patches[pos].set_hatch(hatch)
                                    # ax.patches[pos].set_hatchcolor("red")
                                    # ax.patches[pos].set_facecolor(marker_fc)
                                    # leg = plt.gca().get_legend()
                                    # for marker in marker_list:
                                    #    pos = df.T.columns.get_loc(marker)
                                    #    leg.legendHandles[pos].set_color(marker_fc)
                                    #    leg.legendHandles[pos].set_height(45)
                                    #    leg.legendHandles[pos].set_hatch(marker_hatch)
        ax.legend(loc=loc_leg, bbox_to_anchor=bbox_to_anchor, ncol=ncol)
                                    # leg = plt.gca().get_legend()
                                    # for marker in marker_list:
                                    #    pos = df.T.columns.get_loc(marker)
                                    #    leg.legendHandles[pos].set_hatch(marker_hatch)
                                    # leg.legendHandles[pos].set_color(marker_fc)
                                    # leg.legendHandles[pos].set_height(45)
        ax.set_ylabel(ylabel)
        bpc.marker_ticklabel_by_sample_group(cmap=tick_group_color, number=1000, sample_group=sample2group,
                                                                         sample_order=list(df.index), ax=ax, skip_not_exists=1, axis="xy", recycle_color=1)
                                    # hatch: ['/' | '\\' | '|' | '-' | '+' | 'x' | 'o' | 'O' | '.' | '*']
                                    # if legend_locus == "bottom":
        plt.tight_layout()
        for out in self.outfile:
            plt.savefig(out)
            print(out)

    def line_yscale(self, fontsize=8, figure_width=10, figure_height=5, header=0, index_col=0, sep="\t", dpi=300,
             cmap="Paired",  # tab10 or blue,green,black
             xlabel="", ylabel="", transpose=0, legend_pos="bottom", ncol_legend=1, xlabel_rotation=60, xlabel_font_size=9,
             ha="center",
             va="top",
             tick_group_color="#9b59b6,#3498db",
             title="",
             scale="",
             cutoff="", # "50"
             width_ratios="", # "1,1"
             height_ratios="", # "1,2"
             scale_axis="", # "y"
             sample2group="",
             grid=1):
        df = pd.read_csv(self.data, header=int(header), index_col=int(index_col), sep=sep)
        grid = int(grid)
        if int(transpose):
            df = df.T
        cutoff = fire_table.tablet().parse_tuple(cutoff)
        width_ratios = fire_table.tablet().parse_tuple(width_ratios)
        height_ratios = fire_table.tablet().parse_tuple(height_ratios)
        scale_axis = fire_table.tablet().parse_tuple(scale_axis)
        figure_width = float(figure_width)
        figure_height = float(figure_height)
        cutoffs = [float(i) for i in cutoff.strip().split(",")]
        width_ratios = [float(i) for i in width_ratios.strip().split(",")]
        height_ratios = [float(i) for i in height_ratios.strip().split(",")]
        grid_row = grid_col = 1
        if scale_axis == "y":
            if len(cutoffs)+1 != len(height_ratios):
                print(f"error y:{len(cutoffs)}+1 != {len(height_ratios)}")
                sys.exit(1)
            grid_row = len(cutoffs) + 1
            grid_col = 2
        elif scale_axis == "x":
            if len(cutoffs)+1 != len(width_ratios):
                print("error x")
                sys.exit(1)
            grid_row = 2
            grid_col = len(cutoffs) + 1
        else:
            print(f"error: not support ${scale_axis}")
            sys.exit(1)
        figure = plt.figure(figsize=(figure_width, figure_height))
        gs = gridspec.GridSpec(grid_row, grid_col,
                                      width_ratios=width_ratios,
                                      height_ratios=height_ratios
                                      )
        if not title:
            title = self.data
        if scale_axis == "y":
            min_y = df.values.min()
            max_y = df.values.max()
            gs.update(left=0.55, right=0.98, hspace=0)
            for i in range(len(cutoffs)+1):
                ax = plt.subplot(gs[len(cutoffs)-i, 0])
                df.plot(ax=ax)
                ax.get_legend().remove()
                if i < len(cutoffs):
                    y_max = cutoffs[i]
                else:
                    y_max = max_y
                ax.set_ylim([min_y, y_max])
                min_y = y_max
                if grid:  ax.grid(True)
            ax = plt.subplot(gs[:, 1])
            df.plot(ax=ax)
            ax.legend(loc='center left', bbox_to_anchor=(1.03,0.5))
            if grid:  ax.grid(True)
            plt.title(title)
        else:
            gs.update(left=0.55, right=0.98, vspace=0)
            print("not support x yet")
            sys.exit(1)
        for out in self.outfile:
            figure.savefig(out, dpi=dpi, bbox_inches='tight')
            print(out)

    def line(self,
                fontsize=8, figure_width=0, figure_height=5, header=0, index_col=0, sep="\t", dpi=300,
                cmap="Paired",  # tab10 or blue,green,black
                xlabel="", ylabel="", transpose=0, legend_pos="bottom", ncol_legend=1, xlabel_rotation=60, xlabel_font_size=9,
                ha="center",
                va="top",
                tick_group_color="#9b59b6,#3498db",
                title="",
                scale="",
                sample2group="",
                grid=1):
        df = pd.read_csv(self.data, header=header,
                         index_col=index_col, sep=sep)
        if int(transpose):
            df = df.T
        grid = int(grid)
        linestyles = ['-', '--', '-.', ':']
        columns = df.columns
        figure_width, figure_height = bpc.get_fsize(len(columns), figure_width, figure_height)
        figure = plt.figure(figsize=(figure_width, figure_height))
        xlabel_font_size = float(xlabel_font_size)
        xlabel_rotation = int(xlabel_rotation)
        ncol_legend = int(ncol_legend)
        colors_list = bpc.get_hex_colors_list(cmap=cmap)
        marker_styles = bpc.line_style(colors=colors_list)
        for s in df.index:
            x = columns
            y = df.loc[s]
            if len(marker_styles) == 0:
                    marker_styles = marker_style.copy()
                    marker, style, color = marker_styles.pop(0)
                    plt.plot(x, y, linestyle=style, label=s,
                             marker=marker, color=color)

        legend_loc = ""
        bbox_to_anchor = ()
        if legend_pos == "bottom":
            legend_loc = 'upper center'
            bbox_to_anchor = (0.5, -0.22)
        elif legend_pos == "right":
            legend_loc = 'center left'
            bbox_to_anchor = (1.01, 0.5)
        else:
            print(f"error, not support{legend_pos}, only bottom or right")
            sys.exit(1)
        line_egend = plt.legend(loc=legend_loc, bbox_to_anchor=bbox_to_anchor, ncol=ncol_legend)
        locus = list(range(len(columns)))
        plt.xticks(locus, columns,  rotation=xlabel_rotation, ha=ha, va=va, fontsize=xlabel_font_size)
        ax = plt.gca()
        bpc.marker_ticklabel_by_sample_group(cmap=tick_group_color, number=1000, sample_group=sample2group,
                                             sample_order=list(df.columns)+list(df.index), ax=ax, skip_not_exists=1, axis="x", recycle_color=1)
        ax.add_artist(line_egend)
        if xlabel:
            ax.set_xlabel(xlabel)
        if ylabel:
            ax.set_ylabel(ylabel)
        if scale:
            plt.yscale(scale)
        if not title:
            title = self.data
        plt.title(title)
        if grid:
            ax.grid(True)
        for out in self.outfile:
            figure.savefig(out, dpi=dpi, bbox_inches='tight')
            print(out)

    def heatmap_homemade(self, header=0, index_col=0, sep="\t", linewidths=0, dpi=200, oformat="pdf", cmap="vlag",
                         order_x="", order_y="", xlabel_rotation=90, ylabel_rotation=0, legend_ncol=1,
                         color_segments="red,black,green", value_segments="0:10,10:30,30:100"):
        # read data
        df = pd.read_csv(self.data, header=header,
                         index_col=index_col, sep=sep)
        flatui = ["#9b59b6", "#3498db", "#e74c3c", "#34495e", "#2ecc71"]
        cmap = sns.color_palette(flatui)

        # sort by x or y
        if order_x:
            print(order_x)
            order_x = order_x.strip().strip(",").split(",")
            df = df[order_x]
            if order_y:
                order_y = ",".join(order_y)
                print(order_y)
                order_y = order_y.strip().strip(",").split(",")
                df = df.loc[order_y, :]
                print(
                    f"max value is {df.max().max()}, min value is {df.min().min()}")
                # plot main axes framework
                figure, ax = plt.subplots()
                xlocus = list(range(len(df.columns)))
                plt.xlim(0, len(df.columns))
                xlocus = [i+0.5 for i in xlocus]
                plt.xticks(xlocus, df.columns, rotation=float(xlabel_rotation))

        ylocus = list(range(len(df.index)))
        plt.ylim(0, len(df.index))
        ylocus = [i+0.5 for i in ylocus]
        plt.yticks(ylocus, df.index, rotation=float(ylabel_rotation))

        # plot single cell
        # color_segments="red,black,green", value_segments="0:10,10:30,30:100"):
        if not re.match("#", color_segments):
           sys.exit(print("error:color_segments should be start with #, example #F5DEB3") or 1)
        color_segments = str(color_segments).strip().split(",")
        self.value_segments = str(value_segments).strip().split(",")
        if len(color_segments) != len(self.value_segments):
            sys.exit(print(f"{color_segments} length is {len(color_segments)}, but {value_segments} length is {len(self.value_segments)}") or 1)

        for ix, x in enumerate(df.columns):
            for iy, y in enumerate(df.index):
                cell_value = float(df[x][y])
                color_value = zip(color_segments, self.value_segments)
                cell_bg = self.get_color_heatmap_homemade(
                    cell_value, color_value)
                cell = self.make_cell_heatmap_homemade(
                    ix, iy, 1, 1, cell_bg, 1)
                ax.add_patch(cell)
                ax.grid(False)

        # plot legend
        legends = []
        color_value = zip(color_segments, self.value_segments)
        for color, value in color_value:
            value = re.sub(":", ' - ', value)
            p = patches.Patch(color=color, label=value)
            legends.append(p)
            lgd = ax.legend(handles=legends, ncol=int(legend_ncol), loc='center left', bbox_to_anchor=(1, 0.5))
        for out in self.outfile:
                figure.savefig(out, dpi=dpi, bbox_extra_artists=(
                    lgd,), bbox_inches='tight')
                print(out)

    def make_cell_heatmap_homemade(self, x, y, width, height, color, linewidth):
        cell = patches.Rectangle(
                        (x, y),   # (x,y)
                        width,  # width
                        height,  # height
                        color=color,  # up chr arm color
                        linewidth=linewidth,
                        ec="white"
        )
        return cell

    def get_color_heatmap_homemade(self, cell_value, color_value):
        for color, value in color_value:
            s, e = [float(i) for i in value.split(":")]
            if cell_value >= s and cell_value < e:
                color_bg = color
                return color
        sys.exit(
            print(f"error,{cell_value} is more than {self.value_segments}") or 1)

    def clustermap(self, header=0, index_col=0, sep="\t", add_colorbar_col=0, add_colorbar_row=0, linewidths=0,
                   dpi=200, oformat="pdf", cmap="vlag", method="average", metric="euclidean",
                   tick_group_color="#9b59b6,#3498db",
                   sample2group="",
                   row_cluster=1, col_cluster=1):
        # http://seaborn.pydata.org/examples/structured_heatmap.html
        # cmap = sns.color_palette("Set2", 8)
        # cmap = "icefire_r"
        # cmap = palettable.tableau.GreenOrange_6.mpl_colors
        # flatui = ["#9b59b6", "#3498db", "#e74c3c", "#34495e", "#2ecc71"]
        # cmap = sns.color_palette(flatui,8)
        if int(col_cluster):
            col_cluster = True
        else:
            col_cluster = False
        if int(row_cluster):
            row_cluster = True
        else:
            row_cluster = False
        df = pd.read_csv(self.data, header=header,
                                 index_col=index_col, sep=sep)
        if int(add_colorbar_col):
            col_colors = sns.color_palette("muted", len(df.columns))
        else:
            col_colors = None
        if int(add_colorbar_row):
            row_colors = sns.color_palette("muted", len(df.index))
        else:
            row_colors = None
        plot = sns.clustermap(df,  # center=3,
                                              row_colors=row_colors,
                                              col_colors=col_colors,
                                              method=method, metric=metric,
                                              cmap=cmap,
                                              linewidths=linewidths,
                                              row_cluster=row_cluster,
                                              col_cluster=col_cluster)
        plot.ax_heatmap.set_ylabel("")
        ax = plot.ax_heatmap
        bpc.marker_ticklabel_by_sample_group(cmap=tick_group_color, number=1000, sample_group=sample2group,
                                  sample_order=list(df.columns)+list(df.index), ax=ax, skip_not_exists=1, axis="xy", recycle_color=1)
        for out in self.outfile:
            plot.savefig(out, dpi=dpi)
            print(out)


if __name__ == "__main__":
    fire.Fire(sns_ploter)
