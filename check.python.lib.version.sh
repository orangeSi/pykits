if [ "$1" == "" ];
then
	echo "$0 *py"
	exit
fi
#set -vex
#pip freeze > pip.freeze.out
echo '
#### python package dependence:
```'

cat $1|grep -E '^import|^from'|awk '{print $2}'|sed 's/\..*//'|sort -u|while read lib;
do
	if [ "$lib" == "re" ] || [ "$lib" == "os" ] || [ "$lib" == "sys" ] || [ "$lib" == "time" ] || [ "$lib" == "datetime" ] || [ "$lib" == "gzip" ];
	then
		continue
	fi
	cat pip.freeze.out|grep -iE "$lib"|sed 's/==/ >= /'
done
python -V

echo '```'
