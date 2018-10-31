#!/usr/bin/env python
#-*- coding:UTF-8 -*-
import os
import sys
import gzip
import datetime
import time
import re
import fire
from Bio import SeqIO
from Bio.Seq import Seq


def show_time():
    return datetime.datetime.now()


class AutoVivification(dict):
    """Implementation of perl's autovivification feature."""
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value


class fastakit():
    def __init__(self):
        '''
usage1:
        python *py  filter-fasta-by-head-seq  --fasta input.fa.gz --header AAG --keep 1 --outname out.fa # only sequence which header match AAG will be output

usage2: if you upload genome to ncbi, and ncbi told your genome has some base is alignment to adapter,
            after you validate that and want to replace the region with N, you can:
                blast adapter.fa to your genome get m6 output, cat m6|awk '{print $2","$9","$10}' >adapter.to.assembly.m6.replace.list
                python *py replace_base  --seq_pos_list adapter.to.assembly.m6.replace.list  --pos_count_from 1 --seq_file assembly.fa --output assembly.new.fa # seq_pos_list is multi line, seprate by ,
                python *py replace_base  --seq_id 3 --pos_start 1 --pos_end 30 --pos_count_from 1 --seq_file assembly.fa --output out.fa

        '''
        pass
    def filter_fasta_by_head_seq(self, fasta=None, header=str, keep=int, outname=str):
        print (f"start filter_fasta_by_head_seq at {show_time()}")
        content = ""
        with gzip.open(fasta, "rt") as handle:
            for record in SeqIO.parse(handle, 'fasta'):
                if re.match(header, str(record.seq)) and keep == 1:# when keep =1, will output sequece which matches header
                    content += ">"+record.id+"\n"+str(record.seq)+"\n"
                if not re.match(header, str(record.seq)) and keep == 0:# when keep =0, will output sequece which not matches header
                    content += ">"+record.id+"\n"+str(record.seq)+"\n"
        open(outname, "w").write(content)
        print (f"end filter_fasta_by_head_seq at {show_time()}")

    def replace_base(self, seq_id=None, pos_start=1, pos_end=2,
                replace_base_with="N", seq_pos_list=None, pos_count_from=0,
                seq_file=None, output="tmp", base_number_one_line=60):
        seq_id = str(seq_id)
        base_number_one_line = int(base_number_one_line)
        replace_base_with = str(replace_base_with)
        seq_pos = self.read_list(seq_pos_list, seq_id, pos_start, pos_end, seq_file)
        seqs = SeqIO.parse(seq_file, 'fasta')
        out = open(output, "w")
        start_time = time.time()
        for record in seqs:
            input_seq = str(record.seq)
            input_seq_id = record.id
            new_seq = ""
            for i in seq_pos:
                if input_seq_id != i.split(",")[0]:
                    continue
                seq_id, pos_start, pos_end = self.init_pos(i, pos_count_from)
                if new_seq: input_seq = new_seq
                new_seq = self.sub_base(pos_start, pos_end, input_seq, replace_base_with)
            if not new_seq: new_seq = input_seq
            new_seq = self.format_line(new_seq, base_number_one_line)
            out.write(f">{input_seq_id}\n{new_seq}\n")
        print (f"done, wirte to {output}")
        end_time = time.time()
        print(f"cost time: {end_time - start_time} s")
        print(show_time())


    def sub_base(self, pos_start, pos_end, input_seq, replace_base_with):
        new_seq = "".join(input_seq[:pos_start])
        new_seq += replace_base_with * (abs(pos_start - pos_end)+1)
        new_seq += "".join(input_seq[pos_end+1:])
        return new_seq
    def format_line(self, new_seq, base_number_one_line):
        p = re.compile(r"(.{"+str(base_number_one_line)+"})")
        new_seq = p.sub(r"\1\n", new_seq).strip()
        return new_seq

    def read_list(self, seq_pos_list,seq_id,pos_start,pos_end, seq_file):
        seq_pos = []
        if seq_pos_list:
            with open(seq_pos_list, "r") as f:
                for line in f:
                    line = line.strip()
                    if line == "" or re.match("#", line): continue
                    arrs = line.split(",")
                    lens = len(arrs)
                    if lens < 3 or lens % 2 !=1:
                        sys.exit(print(f"error: {seq_pos_list} need 3 or 5 or 7 ... columns, got {line} :{lens}\n"))
                    for i in range(lens//2):
                        s = arrs[i*2+1]
                        e = arrs[i*2+2]
                        seq_pos.append(f"{arrs[0]},{s},{e}")
        elif seq_id:
            seq_pos.append(f"{seq_id},{pos_start},{pos_end}")
        return seq_pos
    def init_pos(self, i, pos_count_from):
        shift = 0
        if pos_count_from: shift =1
        pos = i.split(",")
        pos[1] = int(pos[1]) - shift
        pos[2] = int(pos[2]) - shift
        if pos[1] > pos[2]:
            pos[1], pos[2] = pos[2], pos[1]
        return pos




if __name__ == "__main__":
    fire.Fire(fastakit)







