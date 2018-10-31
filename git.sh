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


## for first use git
#git init
#git add *
#git commit -m 'update'
#git remote add origin https://github.com/orangeSi/ClustersPloter.git
#git push -u origin master
#git pull origin master

# config password for git
#git config credential.helper store, store mean forver remember password. git config credential.helper 'cache –timeout=3600' for temperate remember password
# git push orgin master 
# ......
# after this will remember the password

