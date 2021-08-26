import json
from discord.ext import commands, tasks

from .functions import user_died

class backgroundtasks(commands.Cog):
    def __init__(self, client):
        self.client = client
        Currency_Countdown.start(self)
        Reddit_MongoDB_Countdown.start(self)
        Reddit_Json_Reset.start(self)

    def cog_unload(self):
        Currency_Countdown.cancel(self)
        Reddit_MongoDB_Countdown.cancel(self)
        Reddit_Json_Reset.cancel(self)

    @commands.Cog.listener()
    async def on_ready(self):
        print("backgroundtasks.py Loaded!")

########################################################## Data Base Loop ###########################################################
@tasks.loop(seconds = 1)
async def Currency_Countdown(self):
    cluster = self.client.mongodb["Currency"]["Main"]
    list_of_users = cluster.find().sort("id", -1)

    for x in list_of_users:
        if x["lifespan"] < 1: 
            user = await self.client.fetch_user(x["id"])
            await user_died(self, None, user)
        else: 
            cluster.update_one({"id": x["id"]},{"$set":{"lifespan": x["lifespan"] - 1}})

        if x["daily"] != 0:
            cluster.update_one({"id": x["id"]},{"$set":{"daily": x["daily"] - 1}})
        if x["weekly"] != 0:
            cluster.update_one({"id": x["id"]},{"$set":{"weekly": x["weekly"] - 1}})
        if x["monthly"] != 0:
            cluster.update_one({"id": x["id"]},{"$set":{"monthly": x["monthly"] - 1}})

        if x["pray"] == 1: 
            cluster.update_one({"id": x["id"]},{"$set":{"luck": round(x["luck"] - 0.1,1)}})
            cluster.update_one({"id": x["id"]},{"$set":{"pray": 0}})
        elif x["pray"] != 0: 
            cluster.update_one({"id": x["id"]},{"$set":{"pray": x["pray"] - 1}})
    return

@tasks.loop(seconds = 1)
async def Reddit_MongoDB_Countdown(self):
    cluster = self.client.mongodb["Reddit"]["Leaderboard"]
    list_of_subreddits = cluster.find().sort("subrredit", -1)

    for x in list_of_subreddits:
        if x["reset_countdown"] != 0:
            cluster.update_one({"subrredit": x["subrredit"]},{"$set":{"reset_countdown": x["reset_countdown"] - 1}})
        
        if x["reset_countdown"] == 0:
            day = 30
            while day != 0:
                if day == 1: cluster.update_one({"subrredit": x["subrredit"]},{"$set":{f"day{day}": 0}})
                else: cluster.update_one({"subrredit": x["subrredit"]},{"$set":{f"day{day}": x[f"day{day-1}"]}})
                day = day - 1
            cluster.update_one({"subrredit": x["subrredit"]},{"$set":{"reset_countdown": 86400}})
    return

####################################################### Local Data Base Loop ########################################################
@tasks.loop(seconds = 21600) #6 hours
async def Reddit_Json_Reset(self):
    data = {}
    with open("reddit_data.json","w") as f:
        json.dump(data, f)
    return
#####################################################################################################################################
def setup(client):
    client.add_cog(backgroundtasks(client))

