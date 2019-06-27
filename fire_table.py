#!/usr/bin/env python3
#-*- coding:UTF-8 -*-

print("start import lib, you have a break time for few seconds now")
import pandas as pd
import sys
import os
import re
import fire
import datetime
print("end import lib")

#def show_time():
#    return datetime.datetime.now()
def show_time(func):
    def wrapper(*args, **kwargs):
        datetime.datetime.now()
        return func(*args, **kwargs)
    return wrapper

#@show_time
class tablet():
    def __init__(self):
        """
        usage:

        python fire.table.py extract --data Phylum.gt1percent.kruskal.test.txt.new2 --keywords A.S.14d,C.S.7d --extract_row 0 --extract_column 1 --prefix test1 --outdir .
        python fire.table.py extract --data Phylum.gt1percent.kruskal.test.txt.new2 --keywords A.S.14d,C.S.7d --extract_row 0 --extract_column 1 --prefix test1 --header 0 --index_col 0 --outdir .
        python fire.table.py extract --data Phylum.gt1percent.kruskal.test.txt.new2 --keywords_file kw.list --keywords_file_field 0 --extract_column 0 --extract_column 1 --prefix test2 --header 0 --index_col 0
        python fire.table.py extract --data Phylum.gt1percent.kruskal.test.txt.new2 --keywords_file kw.list2 --keywords_file_field 1 --extract_column 0 --extract_column 1 --prefix test3 --header 0 --index_col 0
        python fire.table.py extract --data Phylum.gt1percent.kruskal.test.txt.new3 --keywords A.S.14d,C.S.7d --extract_row 0 --extract_column 1 --prefix test4 --header 0 --index_col 0 --sample2group_fileds 0,1 --sample2group sample2group.txt --sample2group_fileds "0,1" --same_outdir 1 --keep_metadata 1 --skip_not_exists 0
        python fire.table.py parse_order_xy --

        For vcf file, set --data_header_contain_comment 1 will auto reset --header

        """
    def parse_kws(self, keywords, keywords_file, sep, comment, keywords_file_field):
        if (keywords and keywords_file) or (not keywords and not keywords_file):
            sys.exit(print(f"--keywords and --keywords_file must exist only one, keywords is {keywords}, keywords_file is {keywords_file} ~\n") or 1)
        kws = []
        if keywords:
            keywords = self.parse_tuple(keywords)
            kws = keywords.strip().strip(",").split(",")
        else:
            df_kwf = pd.read_csv(keywords_file, header=None, index_col=None, sep=sep, comment=comment)
            kws = df_kwf[keywords_file_field].tolist()
        return kws
    def parse_tuple(self, tuples):
        if type(tuples) is tuple:
            tuples = [ str(i) for i in tuples]
            tuples = ",".join(tuples)
        else:
            tuples = str(tuples)
        return tuples
    def parse_sample2group(self, kws, sample2group, sample2group_fileds, sep,  comment):
        if sample2group:# sample    group_name
            sample2group_fileds = self.parse_tuple(sample2group_fileds)
            sf, gf = [ int(i) for i in sample2group_fileds.strip().split(",")]
            g2s = pd.read_csv(sample2group, header=None, index_col=None, sep=sep, comment=comment)
            #kws = g2s[g2s[gf].isin(kws)][sf].tolist() # will miss the order of raw kws
            #print(f"kws1 is{kws}, gs{gf},sf{sf}")
            kws_i = []
            for i in kws:
                t = g2s[g2s[gf] == i][sf].tolist()
                if t:
                    kws_i +=t
                else:
                    kws_i.append(i)
            kws = kws_i
        print(f"kws:{kws}")
        return kws
    def parse_extract_index(self, extract_index, kws, df, skip_not_exists, data):
        print("start parse_extract_index")
        if extract_index:
            kws_i = [ i for i in kws if i in df.index]
            dull = []
            for i in kws:
                if i not in df.index:
                    dull.append(i)
            if len(dull) >0:
                if skip_not_exists:
                    print(f"skip: {dull} is not exist in {df.index} of {data}")
                else:
                    sys.exit(print(f"error: {dull} is not exist in {df.index} of {data}, you can set --skip_not_exists 1 to ignore this") or 1)
            df = df.loc[kws_i, :]
            print(f"{kws}")
            print("end parse_extract_index")
        return df
    #def parse_extract_column(self, extract_column, kws, df, skip_not_exists, data):
    def parse_args(self, *args):
        if len(args) > 0:
            extract_column, kws, df, skip_not_exists, data = args
        else:
            extract_column, kws, df, skip_not_exists, data = self.extract_column, self,kws, self.df, self.skip_not_exists, self.data
        return extract_column, kws, df, skip_not_exists, data
    def parse_extract_column(self, *args):
        extract_column, kws, df, skip_not_exists, data = self.parse_args(*args)
        if extract_column:
            kws_c = [ i for i in kws if i in df.columns]
            if len(kws_c) == 0:
                sys.exit(print(f"error: kws {kws} total are not in {df.columns} of {data}") or 1)
            dull = []
            for i in kws:
                if i not in df.columns:
                    dull.append(i)
            if len(dull) >0:
                if skip_not_exists:
                    print(f"skip: {dull} is not exist in {df.columns} of {data}")
                else:
                    sys.exit(print(f"error: {dull} is not exist in {df.columns} of {data}, you can set --skip_not_exists 1 to ignore this") or 1)
            df = df[kws_c]
        return df
    def parse_keep_metadata(self, keep_metadata, data_header_contain_comment, data, outfile):
        if keep_metadata or data_header_contain_comment:
            print(f"keep_metadata is {keep_metadata}")
            self.metadata = []
            with open(data) as file:
                for line in file:
                    line  = line.strip()
                    if re.match("#", line):
                        self.metadata.append(line)
                    else:
                        break
            if len(self.metadata) >1 and keep_metadata:
                if data_header_contain_comment:
                    open(outfile, "w").write("\n".join(self.metadata[:-1])+"\n")
                else:
                    open(outfile, "w").write("\n".join(self.metadata)+"\n")

                self.mode = "a"
    def parse_order_xy(self, order_x="", order_y="", data=None, header=0, index_col=0, sep="\t", data_comment="#", outfile=None):
        if type(data) == pd.DataFrame:
            print("get dataframe")
            df = data
        elif data:
            df = pd.read_csv(data, header=int(header), index_col=int(index_col), sep=sep, comment=data_comment)
        else:
            print(f"get worng data, type if {type(data)}")
            sys.exit(1)
        if order_x:
            if type(order_x) is tuple: order_x = ",".join(order_x)
            print (order_x)
            order_x = order_x.strip().strip(",").split(",")
            df = df[order_x]
        if order_y:
            if type(order_y) is tuple: order_y = ",".join(order_y)
            print (order_y)
            order_y = order_y.strip().strip(",").split(",")
            df = df.loc[order_y, :]
        if outfile:
            df.to_csv(outfile, sep="\t", header=True, index=True, mode="w")
            print(f"wirte to {outfile}")
        else:
            return df
    def parse_header(self, data_header_contain_comment, header, data_comment):
        if data_header_contain_comment:
           header = len(self.metadata) -1
           data_comment = None
        return int(header), data_comment
    def extract(self, data=None, data_header_contain_comment=None, keywords=None, keywords_file=None, sample2group=None, extract_row=0, extract_column=0,
            sample2group_fileds="0,1", keywords_file_field=0, header=0, index_col=0, sep="\t", comment="#",
            prefix="test.extract", same_outdir=0, outdir=".", keep_metadata=1, skip_not_exists=0, order_x=None, order_y=None,
            return_data_frame=0, print_on_screen=0, df_mean=0, df_min=0, df_max=0):
        keep_metadata = int(keep_metadata)
        return_data_frame = int(return_data_frame)
        print_on_screen = int(print_on_screen)
        # data_header_contain_comment # column_name[0] if contain #
        if int(same_outdir):
            outdir=data+"."
        else:
            outdir=outdir+"/"
        outfile = outdir+prefix
        self.mode = "w"
        data_comment = comment
        self.parse_keep_metadata(keep_metadata, data_header_contain_comment, data, outfile) # decide if keep metadata in data file
        header,data_comment = self.parse_header(data_header_contain_comment, header, data_comment) # get real --header for different data: vcf, etc
        print (f"header is {header}, data_comment is {data_comment}")

        df = pd.read_csv(data, header=header, index_col=int(index_col), sep=sep, comment=data_comment) # read raw data
        print(f"df type is {type(df)}")
        #print(df.columns)
        column_name = df.columns
        #print(f"df.column is {df.columns}")
        kws = self.parse_kws(keywords, keywords_file, sep, comment, keywords_file_field) # get keywords by --keywords or --keywords_file
        kws = self.parse_sample2group(kws, sample2group, sample2group_fileds, sep, comment) # get keywords(samples) of some group by sample2groups
        df = self.parse_extract_index(extract_row, kws, df, skip_not_exists, data) # extract kws in index
        df = self.parse_extract_column(extract_column, kws, df, skip_not_exists, data) # extract kws in column
        df = self.parse_order_xy(order_x, order_y, data=df) # sort df by order_x or order_y
        if return_data_frame: return df
        #df = df[]
        #print(df.columns)
        df.to_csv(outfile, sep="\t", header=True, index=True, mode=self.mode)
        print(f"done, outfile is {outfile}")
        #if df_mean: print(f"#mean is {}")

        if print_on_screen: print (df)

    def merge(self, files, # file1,file2,file3
            merge_type="outer,inner,join_axes",
            join_axes_file_index=0,
            header=0, index_col=0, sep="\t", comment="#",
            prefix="merge.txt",
            outdir="./",
            fillna=0,
            transpose=""): # 1,0,1
        files = files.split(",")
        dfs = []
        trans = self.get_transpose(transpose.strip(), len(files))

        for i,f in enumerate(files):
            if not os.path.exists(f):
                print(f"error: file {f} not exists")
                sys.exit(1)
            df = pd.read_csv(f, header=int(header), index_col=int(index_col), sep=sep, comment=comment)
            if trans[i]: df = df.T
            dfs.append(df)

        outfile = f"{outdir}/{prefix}"

        for t in merge_type.strip().split(","): # "outer,inner,join_axes"
            if t == "outer" or t == "inner":
                result = pd.concat(dfs, axis=1, join=t)
            elif t == "join_axes":
                result = pd.concat(dfs, axis=1, join_axes=[dfs[int(join_axes_file_index)].index])
            else:
                self.myexit(f"error: not support {t} yet, only support outer,inner,join_axes")
            out = outfile+"."+t
            result.fillna(fillna).to_csv(out, sep="\t", header=True, index=True, mode="w")
            print(f"write to {out} done")

    def get_transpose(self, transpose, num):
        trans = []
        if transpose:
            if len(transpose.split(",")) != num: self.myexit("error: --transpose number should match --file number")
            for t in transpose.split(","): trans.append(t)
        else:
            for t in range(num): trans.append(False)
        return trans
    def myexit(self, info, status=1):
        print(info)
        sys.exit(status)

if __name__ == "__main__":
    fire.Fire(tablet)


