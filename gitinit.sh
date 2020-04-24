# gitinit $1
# $1 is the name of the repository

rm -rf .git/
git init
git remote add origin git@github.com:anlitsai/$1.git
git status
git add .
git commit -m "first commit"
git status
git push -u origin master
