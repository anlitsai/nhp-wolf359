# gitpush.sh $1 $2
# $1 is the name of the repository, $2 is commit message

git remote set-url origin git@github.com:anlitsai/$1.git
git status
git add .
git status
git commit -m $2
git push -u origin master

