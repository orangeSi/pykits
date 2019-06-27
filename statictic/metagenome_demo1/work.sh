
ln -s /ifswh1/BC_PS/sikaiwei/bin/python3/lib/statictic/statistic.py .

set -vex
in=Total_gene_abundance.xls
#echo -e "pearson\nspearman\njaccard"|xargs -L 1 -I {} echo "set -vex;python statistic.py  --infile $in  --prefix $in {}"|sh

gs="67-1,67-1.PCRFREE,67-1.WGS"
/ifswh1/BC_PS/sikaiwei/bin/python3/lib/plot/fire_sns.py heatmap --data $in.jaccard.res.txt --sample2group sample.2group --order_x "$gs" --order_y "$gs" --prefix $in.jaccard.res.txt --annot 1
/ifswh1/BC_PS/sikaiwei/bin/python3/lib/plot/fire_sns.py heatmap --data $in.pearson.correlation.res.txt --sample2group sample.2group --order_x "$gs" --order_y "$gs" --prefix $in.pearson.correlation.res.txt --annot 1

/ifswh1/BC_PS/sikaiwei/bin/python3/lib/plot/fire_sns.py heatmap --data $in.spearmanr.correlation.res.txt --sample2group sample.2group --order_x "$gs" --order_y "$gs" --prefix $in.spearmanr.correlation.res.txt --annot 1

touch $0.sign
