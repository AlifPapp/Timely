from discord.ext import commands

from .functions import basic_embed

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
    
    # tpurge <ammount>
    @commands.command(aliases=['clear'])
    async def purge(self, ctx, amt: int = 50):
        if ctx.author.guild_permissions.manage_messages:
            await ctx.message.delete()
            c = await ctx.channel.purge(limit=amt)
            await ctx.send(f"Cleared {len(c)} messages", delete_after=3)
        else:
            await ctx.reply(embed = await basic_embed(f"", f"<:danger:848526668024250408> You are missing the permission `manage_messages`.",self.client.Red,""))

#####################################################################################################################################
def setup(client):
    client.add_cog(other(client))
