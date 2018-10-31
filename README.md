# pykits

############################################################################################

### fastakit.py<br>
#### usage:<br>
If you upload genome to ncbi, and ncbi told your genome has some base is alignment to adapter, after you validate that and want to replace the region with N,
you can: blast adapter.fa to your genome get m6 output, cat m6|awk '{print $2","$9","$10}' > adapter.to.assembly.m6.replace.list
```
# --seq_pos_list is multi line, seprate by , 
python fastakit.py replace_base  --seq_pos_list seq_pos_list  --pos_count_from 1 --seq_file assembly.fa --output assembly.new.fa 

# or this just one pos
python fastakit.py replace_base  --seq_id 3 --pos_start 1 --pos_end 30 --pos_count_from 1 --seq_file assembly.fa --output assembly.new.fa
```
#### python package dependence:
```
biopython >= 1.72
fire >= 0.1.3
Python 3.6.1 :: Anaconda custom (64-bit)
```
<br>
<br>
############################################################################################
### fire_table.py<br>
#### for metagenome/16s/vcf or other data process:
```
# extract column or row or both by keywords, also support extrac sample name by group name
python fire_table.py extract --data Phylum.gt1percent.kruskal.test.txt.new3 --keywords A.S.14d,C.S.7d --extract_index 0 \
	--extract_column 1 	--prefix test4 --header 0 --index_col 0 --sample2group_fileds 0,1 --sample2group sample2group.txt \
	--sample2group_fileds "0,1" --same_outdir 1 --keep_metadata 1 --skip_not_exists 0
```

#### python package dependence:
```
fire >= 0.1.3
pandas >= 0.23.4
Python 3.6.1 :: Anaconda custom (64-bit)
```
