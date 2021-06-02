import discord
from discord import Permissions
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions

from datetime import datetime

from discord.ext.commands.core import guild_only



class moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("moderation.py Loaded!")

    async def cog_check(self, ctx):
        if ctx.guild is not None: return True
        if not ctx.author.bot: return True\
    
    # tgiveadmin <name>
    @commands.command()
    async def giveadmin(self, ctx, user: discord.Member = None):
        if ctx.guild is None:
            return
        if ctx.author.guild_permissions.administrator:
            guild = ctx.guild
            if user is None:
                em = discord.Embed(description = f"<:danger:848526668024250408> No user was specified.",
                                   color = self.client.Red,
                                   timestamp=datetime.utcnow())
                await ctx.reply(embed = em)
                return
            
            role = await guild.create_role(name="Admin",permissions=Permissions.all())  
            await user.add_roles(role)
            em = discord.Embed(description = f":info:848526617449070633> {user.mention} received the role {role.mention}",
                               color = self.client.Red,
                               timestamp=datetime.utcnow())
            await ctx.send(embed = em)
        else:
            em = discord.Embed(description = f"<:danger:848526668024250408> You are missing the permission `administrator`.",
                               color = self.client.Red,
                               timestamp=datetime.utcnow())
            await ctx.reply(embed = em)


    # tpurge <ammount>
    @commands.command(aliases=['clear'])
    async def purge(self, ctx, amt: int = 50):
        if ctx.guild is None:
            return
        if ctx.author.guild_permissions.manage_messages:
            await ctx.message.delete()
            c = await ctx.channel.purge(limit=amt)
            await ctx.reply(f"Cleared {len(c)} messages", delete_after=3)
        else:
            em = discord.Embed(description = f"<:danger:848526668024250408> You are missing the permission `manage_messages`.",
                               color = self.client.Red,
                               timestamp=datetime.utcnow())
            await ctx.reply(embed = em)


    
    @commands.command()
    async def ban(self, ctx, user: discord.Member = None, reason: str=None, delete_message_days: int=0):
        if ctx.guild is None:
            return
        if ctx.author.guild_permissions.ban_members:
            if user is None:
                em = discord.Embed(description = f"<:danger:848526668024250408> No user was specified.",
                                   color = self.client.Red,
                                   timestamp=datetime.utcnow())
                await ctx.reply(embed = em)
                return
            guild = ctx.guild
            #try to ban user
            try:
                await user.guild.ban(user=user,reason=reason,delete_message_days=delete_message_days)
            except discord.Forbidden:
                em = discord.Embed(description = f"<:danger:848526668024250408> I do not have the permission to ban this user`.",
                                   color = self.client.Red,
                                   timestamp=datetime.utcnow())
                await ctx.reply(embed = em)
                return

            #ban message
            em = discord.Embed(title = "The BAN HAMMER has striked down on another poor soul.",
                               description = f":info:848526617449070633> {user} has been banned! \nReason: {reason} \nDelete_messages_days: {delete_message_days}",
                               color = self.client.Red,
                               timestamp=datetime.utcnow())

            await ctx.reply(embed = em)
        else:
            em = discord.Embed(description = f"<:danger:848526668024250408> You are missing the permission `ban_members`.",
                               color = self.client.Red,
                               timestamp=datetime.utcnow())
            await ctx.reply(embed = em)

    # tunban <userid>
    @commands.command()
    async def unban(self, ctx, userid: int=0):
        if ctx.guild is None:
            return
        if userid == 0:
            em = discord.Embed(description = f"<:danger:848526668024250408> No user id was specified.",
                               color = self.client.Red,
                               timestamp=datetime.utcnow())
            await ctx.reply(embed = em)
            return
        # Fetch user from id
        try:
            user = await self.client.fetch_user(userid)
        except discord.NotFound:
            em = discord.Embed(description = "<:danger:848526668024250408> Invalid id, user not found.",
                               color = self.client.Red,
                               timestamp=datetime.utcnow())

            await ctx.reply(embed = em)
            return
        except discord.HTTPException:
            em = discord.Embed(description = "<:danger:848526668024250408> Fetching the user failed.",
                               color = self.client.Red,
                               timestamp=datetime.utcnow())

            await ctx.reply(embed = em)
            return

         # Check if userid is a banned user
        targetguild = ctx.guild
        Check = await is_banned(ctx, user, targetguild)

         # If userid is a banned user
        if Check == True:
            await targetguild.unban(user)
            em = discord.Embed(description = f"<:info:848526617449070633> {user} has been unbaned from {targetguild.name}.",
                               color = self.client.Red,
                               timestamp=datetime.utcnow())

            await ctx.reply(embed = em)
        else:
            em = discord.Embed(description = f"<:danger:848526668024250408> {userid} is not found as banned users from {targetguild.name}.",
                               color = self.client.Red,
                               timestamp=datetime.utcnow())

            await ctx.reply(embed = em)
            return
        

async def is_banned(ctx, user, targetguild):
    banned_users = await targetguild.bans()
    for ban_entry in banned_users:
        if user == ban_entry.user:
            return True



#####################################################################################################################################
def setup(client):
    client.add_cog(moderation(client))