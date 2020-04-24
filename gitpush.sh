name='nhp-wolf359'
datetime=`date +%Y%m%d-%H%M`
comment='update_'$datetime
# gitpush.sh $name $comment
# $name is the name of the repository, $comment is commit message

git remote set-url origin git@github.com:anlitsai/$name.git
git status
git add .
git status
git commit -m $comment
git push -u origin master

