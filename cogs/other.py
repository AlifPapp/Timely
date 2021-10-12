import json

from discord import Embed
from discord.ext import commands
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
        command_syntax = f"Syntax: {self.client.serverprefix}purge <ammount>"
        if ctx.author.guild_permissions.manage_messages:
            await ctx.message.delete()
            c = await ctx.channel.purge(limit=amt)
            await ctx.send(f"Cleared {len(c)} messages", delete_after=3)
        else:
            await ctx.reply(embed = await basic_embed(f"", f"{self.client.Emojis['danger']} You are missing the permission `manage_messages`.",self.client.Red,f"{command_syntax}"))
    
    # tsendembed <json string>
    @commands.command()
    async def send(self, ctx, *, content: str):
        command_syntax = f"Syntax: {self.client.serverprefix}sendembed <json_string>"
        try: 
            content = json.loads(content)
        except: 
            await ctx.reply(embed = await basic_embed(f"", f"{self.client.Emojis['danger']} Failed to load json string.",self.client.Red,f"{command_syntax}"))
            return
        try:
            em = Embed().from_dict(content['embed'])
            await ctx.send(content=content['content'], embed = em)
        except:
            await ctx.reply(embed = await basic_embed(f"", f"{self.client.Emojis['danger']} Failed to construct.",self.client.Red,f"{command_syntax}"))

#####################################################################################################################################
def setup(client):
    client.add_cog(other(client))