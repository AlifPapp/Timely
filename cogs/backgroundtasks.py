from discord.ext import commands, tasks

from .functions import user_died

class backgroundtasks(commands.Cog):
    def __init__(self, client):
        self.client = client
        Loop_ticktock.start(self)

    def cog_unload(self):
        Loop_ticktock.cancel(self)

    @commands.Cog.listener()
    async def on_ready(self):
        print("backgroundtasks.py Loaded!")

#####################################################################################################################################
############################################################## L O O P S ############################################################
#####################################################################################################################################
@tasks.loop(seconds = 1)
async def Loop_ticktock(self):
    await self.client.wait_until_ready()
    cluster = self.client.mongodb["Currency"]["Main"]
    list_of_users = cluster.find().sort("id", -1)

    for x in list_of_users:
        if x["lifespan"] < 1: 
            user = await self.client.fetch_user(x['id'])
            await user_died(self, None, user)
        else: cluster.update_one({"id":x['id']},{"$set":{"lifespan":x["lifespan"] - 1}})

        if x["daily"] != 0:
            cluster.update_one({"id":x['id']},{"$set":{"daily":x["daily"] - 1}})
        if x["weekly"] != 0:
            cluster.update_one({"id":x['id']},{"$set":{"weekly":x["weekly"] - 1}})
        if x["monthly"] != 0:
            cluster.update_one({"id":x['id']},{"$set":{"monthly":x["monthly"] - 1}})

    return

#####################################################################################################################################
def setup(client):
    client.add_cog(backgroundtasks(client))

