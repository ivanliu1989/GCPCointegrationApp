#Create local git
git init
#Add all things in the current directory to the local git
git add .
#Add a remote repository
git remote add https://Piyapong_4507075@bitbucket.org/Piyapong_4507075/gcgcointegration.git
#Commit with comments
git commit -m "Initial version"
#Push to a remote repository
git push origin master

#Optional force push to a remote repository
git push -f origin master
