from discord.ext import commands
from discord.ext.commands import CommandNotFound

class error(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("error.py Loaded!")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
            if isinstance(error, CommandNotFound):
                return
            raise error

#####################################################################################################################################
def setup(client):
    client.add_cog(error(client))