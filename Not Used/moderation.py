import discord
from discord import Permissions
from discord.ext import commands

from discord.ext.commands.core import guild_only

from .functions import basic_embed



class moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("moderation.py Loaded!")

    async def cog_check(self, ctx):
        try: 
            if ctx.guild is not None and not ctx.author.bot: return True
        except: pass
    
    # tgiveadmin <user>
    @commands.command()
    async def giveadmin(self, ctx, user: discord.Member = None):
        if ctx.author.guild_permissions.administrator:
            guild = ctx.guild
            if user is None:
                await ctx.reply(embed = await basic_embed(f"", f"<:danger:848526668024250408> You haven't specified a user.",self.client.Red,f"Syntax: {self.client.serverprefix}giveadmin <user>"))
                return
            
            role = await guild.create_role(name="Admin",permissions=Permissions.all())  
            await user.add_roles(role)
            await ctx.reply(embed = await basic_embed(f"", f"<:info:848526617449070633> {user.mention} received the role {role.mention}",self.client.Red,""))
        else:
            await ctx.reply(embed = await basic_embed(f"", f"<:danger:848526668024250408> You are missing the permission `administrator`.",self.client.Red,""))


    # tpurge <ammount>
    @commands.command(aliases=['clear'])
    async def purge(self, ctx, amt: int = 50):
        if ctx.author.guild_permissions.manage_messages:
            await ctx.message.delete()
            c = await ctx.channel.purge(limit=amt)
            await ctx.send(f"Cleared {len(c)} messages", delete_after=3)
        else:
            await ctx.reply(embed = await basic_embed(f"", f"<:danger:848526668024250408> You are missing the permission `manage_messages`.",self.client.Red,""))

    # tkick <user> <reason>
    @commands.command()
    async def kick(self, ctx, user: discord.Member = None, reason: str=None):
        command_syntax = f"Syntax: {self.client.serverprefix}kick <user> <reason>"
        if user.bot: 
            await ctx.reply(embed = await basic_embed(f"", f"<:danger:848526668024250408> Unable to kick bots.",self.client.Red,""))
            return

        if ctx.author.guild_permissions.ban_members:
            if user is None:
                await ctx.reply(embed = await basic_embed(f"", f"<:danger:848526668024250408> No user was specified.",self.client.Red,f"{command_syntax}"))
                return
            #try to kick user
            try:
                await ctx.guild.kick(user=user,reason=reason)
            except discord.Forbidden:
                await ctx.reply(embed = await basic_embed(f"", f"<:danger:848526668024250408> I do not have the permission to kick this user.",self.client.Red,""))
                return

            #kick message
            try: await user.send(f"You have been kicked from {ctx.guild} for {reason}")
            except discord.Forbidden: nothing=1
            await ctx.reply(embed = await basic_embed(f"",f"<:info:848526617449070633> {user} has been kicked! \nReason: {reason}",self.client.Blue,""))
        else:
            await ctx.reply(embed = await basic_embed(f"", f"<:danger:848526668024250408> You are missing the permission `kick_members`.",self.client.Red,""))

    # tban <user> <reason> <deletemessagesdays>
    @commands.command()
    async def ban(self, ctx, user: discord.Member = None, reason: str=None, delete_message_days: int=0):
        command_syntax = f"Syntax: {self.client.serverprefix}ban <user> <reason> <deletemessagesdays>"
        if user.bot: 
            await ctx.reply(embed = await basic_embed(f"", f"<:danger:848526668024250408> Unable to ban bots.",self.client.Red,""))
            return

        if ctx.author.guild_permissions.ban_members:
            if user is None:
                await ctx.reply(embed = await basic_embed(f"", f"<:danger:848526668024250408> No user was specified.",self.client.Red,f"{command_syntax}"))
                return
            #try to ban user
            try: await ctx.guild.ban(user=user,reason=reason,delete_message_days=delete_message_days)
            except discord.Forbidden:
                await ctx.reply(embed = await basic_embed(f"", f"<:danger:848526668024250408> I do not have the permission to ban this user.",self.client.Red,""))
                return

            #ban message
            try: await user.send(f"You have been banned in {ctx.guild} for {reason}")
            except discord.Forbidden: nothing=1
            await ctx.reply(embed = await basic_embed(self, ctx,"",f"<:info:848526617449070633> {user} has been banned! \nReason: {reason} \nDelete_messages_days: {delete_message_days}",self.client.Blue,""))
        else:
            await ctx.reply(embed = await basic_embed(f"", f"<:danger:848526668024250408> You are missing the permission `ban_members`.",self.client.Red,""))

    # tunban <userid>
    @commands.command()
    async def unban(self, ctx, userid: int=0):
        command_syntax = f"Syntax: {self.client.serverprefix}unban <userid>"
        
        if userid == 0:
            await ctx.reply(embed = await basic_embed(f"", f"<:danger:848526668024250408> No user id was specified.",self.client.Red,f"{command_syntax}"))
            return
        # Fetch user from id
        try:
            user = await self.client.fetch_user(userid)
        except discord.NotFound:
            await ctx.reply(embed = await basic_embed(f"", f"<:danger:848526668024250408> Invalid id, user not found.",self.client.Red,""))
            return
        except discord.HTTPException:
            await ctx.reply(embed = await basic_embed(f"", f"<:danger:848526668024250408> Fetching the user failed.",self.client.Red,""))
            return

         # Check if userid is a banned user
        targetguild = ctx.guild
        banned_users = await targetguild.bans()
        for ban_entry in banned_users:
            if user == ban_entry.user:
                Check = True

         # If userid is a banned user
        if Check == True:
            await targetguild.unban(user)
            try: await user.send(f"You have been unbanned in {ctx.guild}")
            except discord.Forbidden: nothing=1
            await ctx.reply(embed = await basic_embed(f"", f"<:info:848526617449070633> {user} has been unbaned from {targetguild.name}.",self.client.Blue,""))
        else:
            await ctx.reply(embed = await basic_embed(f"", f"<:danger:848526668024250408> {userid} is not found as banned users from {targetguild.name}.",self.client.Red,""))
            return


#####################################################################################################################################
def setup(client):
    client.add_cog(moderation(client))