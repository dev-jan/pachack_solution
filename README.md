# PacHack solution "1. Platz"

This AI-bot was developed for the "Pac-hack" hackathon (organised by STAIR - the student 
organization at HSLU). This bot win the first place :trophy:

![Screenshot PacHack](screenshot.png)

The logic of the bot is based on the well-known shortest path algorithm A* (Explained here:
http://bryukh.com/labyrinth-algorithms/).

Authors of the bot:
 - Brian Boss ([@Lextum](https://github.com/Lextum))
 - Jan Bucher ([@dev-jan](https://github.com/dev-jan))

Special thanks to the members of STAIR for organizing this amazing hackathon!

_Disclaimer: This bot was implemented in just one day at a hackathon, don't expect the
code to follow all clean code standards_ :poop:

#### Requirements

* a working Python 3.6 development environment ([getting started guide](http://hackercodex.com/guide/python-development-environment-on-mac-osx/))
* experience [deploying Python apps to Heroku](https://devcenter.heroku.com/articles/getting-started-with-python#introduction)
* [pip](https://pip.pypa.io/en/latest/installing.html) to install Python dependencies

## Running the PacHack game locally

1) Clone repo to your development environment:
```
git clone git@github.com:dev-jan/pachack_solution.git
```

2) Install dependencies using [pip](https://pip.pypa.io/en/latest/installing.html):
```
pip install -r requirements.txt
```

3) Run local server:
```
python3 -m app
```

4) Test client in your browser: [http://localhost:8080](http://localhost:8080).

5) Download the game client to host a new game from the STAIR repo:
https://github.com/stairch/hslu_18hs_stair_pachack_python_local_game (this bot only works
with the version 0.7 of the pachack game).

6) Configurate the bots used by the game in the settings.ini file. Example to run the
local bot against the STAIR bot:
```
[RedTeam]
members = http://localhost:8080
[BlueTeam]
members = https://pachack-stairbot.herokuapp.com
```

## Deploying bot to Heroku

1) Create a new Heroku app (On Windows use Commandline or PowerShell):
```
heroku create [APP_NAME] --region eu
```

2) Deploy code to Heroku servers:
```
git push heroku master
```

3) Open Heroku app in browser:
```
heroku open
```
or visit [http://APP_NAME.herokuapp.com](http://APP_NAME.herokuapp.com).

4) View server logs with the `heroku logs` command:
```
heroku logs --tail
```
