# pykits

### fastakit.py<br>
#### usage1:<br>
If you upload genome to ncbi, and ncbi told your genome has some base is alignment to adapter, after you validate that and want to replace the region with N,
you can: blast adapter.fa to your genome get m6 output, cat m6|awk '{print $2","$9","$10}' > adapter.to.assembly.m6.replace.list
```
	# --seq_pos_list is multi line, seprate by , 
	python fastakit.py replace_base  --seq_pos_list seq_pos_list  --pos_count_from 1 --seq_file assembly.fa --output assembly.new.fa 
	# or this just one pos
	python fastakit.py replace_base  --seq_id 3 --pos_start 1 --pos_end 30 --pos_count_from 1 --seq_file assembly.fa --output assembly.new.fa
```

#####################################################################################################################################

