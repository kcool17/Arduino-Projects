cd C:\Users\kcool\Documents\Github\personal_projects\discord_bots\sawickipedia.exe\my-bot
call heroku login
call heroku git:remote -a polar-temple-11631
set /p CommitName=What do you want to call the commit?
call git add .
call git commit -m "%CommitName%"
call git push heroku master
call heroku scale worker=1
pause