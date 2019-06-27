#!/ifswh1/BC_PS/sikaiwei/software/conda/anaconda3/bin/python
from biom import load_table
import fire

def ab2relative(biomfile, outfile):
    print(f"start to read {biomfile}")
    table = load_table(biomfile)
    tsv = table.norm(axis='sample', inplace=False).to_tsv()
    open(outfile, "w").write(tsv)
    print(f"done, write to {outfile}")

if __name__ == "__main__":
    #fire.Fire(ab2relative)
    fire.Fire()
