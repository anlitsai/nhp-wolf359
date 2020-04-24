name='nhp-wolf359'
comment=$1
# gitpush.sh $name $comment
# $name is the name of the repository, $comment is commit message

git remote set-url origin git@github.com:anlitsai/$name.git
git status
git add .
git status
git commit -m $comment
git push -u origin master

