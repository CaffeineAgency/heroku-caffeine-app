@echo off
set /P comm_mess="Commit message: "
git add .
git commit -am "%comm_mess%"
git push
exit