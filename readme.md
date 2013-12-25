#FaLaLaLaBot 
**A Twitter Bot by Daniel Plemmons**

**NOTE:** This was written on Christmas-Eve in a rush. Probably not the best code ever.

FaLaLaLaBot is a very simple twitter bot that finds tweets once per hour where the poster has said "Tis the season to be..."  and reposts it with a FaLaLaLaLa. It trys to avoid things it has said before (though it isn't great at it.)

**Additional Requirements:**
- python-twitter: https://github.com/bear/python-twitter.
- A twitter account with an active application attached.
- a config.py with your login credentials.

**Running:**
I personally run the bot on a ubuntu virtual box. To start the bot in the background and not let the process get killed upon ending the ssh session I use:

    nohup python falalalabot.py > /dev/null < /dev/null &!
