import json
from typing import Optional
import discord

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
        if ctx.author.guild_permissions.manage_messages:
            await ctx.message.delete()
            c = await ctx.channel.purge(limit=amt)
            await ctx.send(f"Cleared {len(c)} messages", delete_after=3)
        else:
            await ctx.reply(embed = await basic_embed(f"", f"{self.client.Emojis['danger']} You are missing the permission `manage_messages`.",self.client.Red,f""))
    
    # tsendembed <json string>
    @commands.command()
    async def send(self, ctx, *, json_string: str):
        command_syntax = f"Syntax: {self.client.serverprefix}sendembed <json_string>"
        try: 
            json_data = json.loads(json_string)
        except: 
            await ctx.reply(embed = await basic_embed(f"", f"{self.client.Emojis['danger']} Failed to load json string.",self.client.Red,f"{command_syntax}"))
            return
        try: 
            content = json_data['content']
            if content == "": 
                content = None
        except: 
            content = None
        try: 
            embed = json_data['embed']
            if embed == "": 
                embed = None
        except: 
            embed = None
        if content is None and embed is None:
            await ctx.reply(embed = await basic_embed(f"", f"{self.client.Emojis['danger']} Can't send an empty message.",self.client.Red,f""))
            return
        if content != None: content = content.replace('@', '`@`')
        
        try:
            if embed is not None: 
                embed = Embed().from_dict(embed)
            await ctx.send(content=content, embed = embed)
        except:
            await ctx.reply(embed = await basic_embed(f"", f"{self.client.Emojis['danger']} Failed to construct.",self.client.Red,f""))
    
    @commands.command()
    async def lock(self, ctx, channel: Optional[discord.TextChannel], role: Optional[discord.Role]):
        if ctx.author.guild_permissions.manage_channels:
            channel = channel or ctx.channel
            role = role or ctx.guild.default_role
            overwrite = channel.overwrites_for(role)
            overwrite.send_messages = False
            await channel.set_permissions(role, overwrite=overwrite)
            await ctx.reply(embed = await basic_embed(f"", f"{self.client.Emojis['lock']} Locked {channel.mention} to {role}.",self.client.Red,f""))
        else:
            await ctx.reply(embed = await basic_embed(f"", f"{self.client.Emojis['danger']} You are missing the permission `manage_channels`.",self.client.Red,f""))
    
    @commands.command()
    async def unlock(self, ctx, channel: Optional[discord.TextChannel], role: Optional[discord.Role]):
        if ctx.author.guild_permissions.manage_channels:
            channel = channel or ctx.channel
            role = role or ctx.guild.default_role
            overwrite = channel.overwrites_for(role)
            overwrite.send_messages = True
            await channel.set_permissions(role, overwrite=overwrite)
            await ctx.reply(embed = await basic_embed(f"", f"{self.client.Emojis['unlock']} Unlocked {channel.mention} to {role}.",self.client.Blue,f""))
        else:
            await ctx.reply(embed = await basic_embed(f"", f"{self.client.Emojis['danger']} You are missing the permission `manage_channels`.",self.client.Red,f""))

#####################################################################################################################################
def setup(client):
    client.add_cog(other(client))