if [ "$1" == "" ];
then
	echo "sh $0 <commit>"
	exit
fi
commit=$1
set -vex
git add * 
git commit -m "$commit"
git push -u origin master
