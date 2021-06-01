# TimelyBot_Official

**Required libary and set up:**

* Download [discord.py](https://pypi.org/project/discord.py/)
* Download ffmpeg
* Run these commands to instal the required modules:
  * `py -3 -m pip install -U discord.py[voice]` Run in CMDPromt
  * `py -m pip install pymongo` Run in vsc terminal
  * `py -m pip install dsnpython` Run in vsc terminal
  * `py -3 -m pip install -U asyncio` Run in CMDPromt
  * `py -3 -m pip install -U youtube_dl` Run in CMDPromt

* HEROKU SETUP
  * `py -m pip freeze > requirements.txt` Run in vsc terminal
  * Add the build packs: 
    * https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest
    * https://github.com/xrisk/heroku-opus
  * Remove any imports that is not used at the start of the script to avoid errors.

**Links:**
* TimelyBot:
  * [Invite](https://discord.com/api/oauth2/authorize?client_id=836198930873057290&permissions=8&scope=bot)
  * [SupportServer](https://discord.gg/E8DnTgMvMW)
* Zseni:
  * [Discord](https://discord.gg/SXng95f)
  * [Youtube](http://bit.ly/Zseni-Youtube)
