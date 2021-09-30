from discord.ext import commands

class other(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("other.py Loaded!")
    
    async def cog_check(self, ctx):
        try: 
            if ctx.guild is not None and not ctx.author.bot: return True
        except: pass
    
    # tdevpurge <ammount>
    @commands.command()
    async def devpurge(self, ctx, l: int = 50):
        if ctx.guild is not None:
            await ctx.message.delete()
            c = await ctx.channel.purge(limit=l)
            await ctx.send(f"Cleared {len(c)} messages", delete_after=3)

#####################################################################################################################################
def setup(client):
    client.add_cog(other(client))