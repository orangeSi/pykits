#!/usr/bin/env python3

from scipy import stats
from scipy.spatial import distance
import pandas as pd
import fire
import os

class statistic():
    def __init__(self, infile=None, prefix='test', outdir="./", sep="\t", header=0, index_col=0, T=False):
        if not os.path.exists(infile):
            print(f"{infile} is not exists,need input --infile")
            sys.exit(1)
        print(f"read {infile} start")
        self.data = pd.read_csv(infile, sep=sep, header=int(header), index_col=int(index_col))
        if T: self.data = self.data.T
        print(self.data.head())
        print(f"read {infile} end ")
        self.prefix = prefix
        self.outdir = outdir
        self.sep = sep
    def jaccard(self, data=None):
        print("jaccard start")
        if not data:
            data = self.data.copy()
            print("copy that")
        res = pd.DataFrame(index=data.columns, columns=data.columns)
        data[data > 0] = 1
        data[data <= 0] = 0
        [sys.exit(print("error: "+name +" has value neither 1 nor 0")) for name in data.columns if not data[(data[name] !=1) & (data[name] !=0)].empty]
        for q in data.columns:
            for t in data.columns:
                if q == t :
                    res[q][t] = 1
                    continue
                res[q][t] = 1 - distance.jaccard(data[q], data[t])
        out = self.outdir+"/"+self.prefix+".jaccard.similarity.res"
        res.to_csv(out+".txt", sep=self.sep)
        print(f"write to {out}*")
        print("jaccard end")
    def pearson(self, data=None):
        print("pearson start")
        data = self.data
        corr = pd.DataFrame(index=data.columns, columns=data.columns)
        ps = pd.DataFrame(index=data.columns, columns=data.columns)
        for q in data.columns:
            for t in data.columns:
                if q == t :
                    corr[q][t] = 1
                    ps[q][t] = 0
                    continue
                correlation, pvalue = stats.stats.pearsonr(data[q], data[t])
                corr[q][t] = correlation
                ps[q][t] = pvalue
        out = self.outdir+"/"+self.prefix+".pearson"
        corr.to_csv(out+".correlation.res.txt", sep=self.sep)
        ps.to_csv(out+".pvalue.res.txt", sep=self.sep)
        print(f"write to {out}*")
        print("pearson end")

    def spearman(self, data=None):
        print("spearman start")
        data = self.data
        corr = pd.DataFrame(index=data.columns, columns=data.columns)
        ps = pd.DataFrame(index=data.columns, columns=data.columns)
        for q in data.columns:
            for t in data.columns:
                if q == t :
                    corr[q][t] = 1
                    ps[q][t] = 0
                    continue
                correlation, pvalue = stats.stats.spearmanr(data[q], data[t])
                corr[q][t] = correlation
                ps[q][t] = pvalue
        out = self.outdir+"/"+self.prefix+".spearmanr"
        corr.to_csv(out+".correlation.res.txt", sep=self.sep)
        ps.to_csv(out+".pvalue.res.txt", sep=self.sep)
        print(f"write to {out}*")
        print("spearmanr end")

if __name__ == "__main__":
    fire.Fire(statistic)
