set -vex
cp ../plot/fire_sns.py .
cp ../plot/baselib/plot_core.py baselib/
cp ../extract_data/fire_table.py .
cp ../fastakit.py .
rsync -arv ../biom-format .
rsync -arv ../statictic .
echo done
