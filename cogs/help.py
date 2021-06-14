import discord
from discord.ext import commands
from datetime import datetime

client = discord.Client

class help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("help.py Loaded!")

    async def cog_check(self, ctx):
        if ctx.guild is not None: return True
        if not ctx.author.bot: return True

    # thelp
    @commands.group(invoke_without_command=True)
    async def help(self, ctx):
        p = self.client.serverprefix
        em = discord.Embed(title = "List of commands",
                           description = f"Prefix: `{p}` and {self.client.user.mention}",
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())

        em.add_field(name="Categories",value=f"> Currency\n> Music\n> Moderation\n> Settings\n> Information",inline=False)
        em.add_field(name="Usage:",value = f"`{p}<help <category>`")

        await ctx.send(embed = em)


    # thelp Currency
    @help.command()
    async def currency(self, ctx):
        p = self.client.serverprefix
        em = discord.Embed(title = "Currency commands",
                           description = "These are the commands for a unique economy system based on the movie `In Time`.",
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())

        em.add_field(name="Commands:",value=f"`{p}balance`, `{p}profile`, `{p}rich`, `{p}pray`, `{p}daily`, `{p}weekly`, `{p}monthly` `{p}work`, `{p}steal`, `{p}give`")

        await ctx.send(embed = em)

    # thelp ModCurrency
    @help.command()
    async def devcurrency(self, ctx):
        p = self.client.serverprefix
        em = discord.Embed(title = "Currency Moderator commands",
                           description = "Commands that can only be used by Timely's moderators.",
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())

        em.add_field(name="Commands:",value=f"`{p}editusercurrency`, `{p}openaccountcurrency`")

        await ctx.send(embed = em)

    # thelp Music
    @help.command()
    async def music(self, ctx):
        p = self.client.serverprefix
        em = discord.Embed(title = "Music commands",
                           description = "Commands for listening to music",
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())

        em.add_field(name="Commands:",value=f"`{p}play`, `{p}pause`, `{p}resume`, `{p}leave`, `{p}join`")

        await ctx.send(embed = em)

    # thelp Moderation
    @help.command()
    async def moderation(self, ctx):
        p = self.client.serverprefix
        em = discord.Embed(title = "Moderation commands",
                           description = "Help moderate your server with these commands.",
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())

        em.add_field(name="Commands:",value=f"`{p}purge`, `{p}giveadmin`, `{p}kick`, `{p}ban`, `{p}unban`")

        await ctx.send(embed = em)

    # thelp Information
    @help.command()
    async def information(self, ctx):
        p = self.client.serverprefix
        em = discord.Embed(title = "Informational commands",
                           description = "commands that returns information on things.",
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())

        em.add_field(name="Commands:",value=f"`{p}prefix`, `{p}ping`, `{p}invite`, `{p}creator`, `{p}developers`, `{p}userinfo`, `{p}serverinfo`, `{p}avatar`, `{p}botinfo`, `{p}oldest`, `{p}newest`")

        await ctx.send(embed = em)

    # thelp Settings
    @help.command()
    async def settings(self, ctx):
        p = self.client.serverprefix
        em = discord.Embed(title = "Config commands",
                           description = "Per-server settings.",
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())

        em.add_field(name="Commands:",value=f"`{p}changeprefix`")

        await ctx.send(embed = em)

#####################################################################################################################################
########################################################## C U R R E N C Y ##########################################################
########################################################### C O M A N D S ###########################################################
#####################################################################################################################################

    # thelp balance
    @help.command(aliases=['bal'])
    async def balance(self, ctx):
        p = self.client.serverprefix
        em = discord.Embed(title = "Balance",
                           description = "Returns your remaining lifespan and savings",
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())
        em.add_field(name="**Syntax**",value=f"`{p}balance <user>`")
        em.add_field(name="**Aliases**",value=f"`{p}balance`, `{p}bal`")

        await ctx.send(embed = em)

    # thelp profile
    @help.command()
    async def profile(self, ctx):
        p = self.client.serverprefix
        em = discord.Embed(title = "Profile",
                           description = "Returns extensive information on a user in TimelyBot",
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())
        em.add_field(name="**Syntax**",value=f"`{p}profile <user>`")

        await ctx.send(embed = em)

    # thelp rich
    @help.command()
    async def rich(self, ctx):
        p = self.client.serverprefix
        em = discord.Embed(title = "Rich",
                           description = "Returns the richest users in the server",
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())
        em.add_field(name="**Syntax**",value=f"`{p}rich <user> <page>`")

        await ctx.send(embed = em)

    # thelp pray
    @help.command()
    async def pray(self, ctx):
        p = self.client.serverprefix
        em = discord.Embed(title = "Pray",
                           description = "Beg **GOD** for good health",
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())
        em.add_field(name="**Syntax**",value=f"`{p}pray <user>`")

        await ctx.send(embed = em)

    # thelp daily
    @help.command()
    async def daily(self, ctx):
        p = self.client.serverprefix
        em = discord.Embed(title = "Daily",
                           description = "Receive your daily reward",
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())
        em.add_field(name="**Syntax**",value=f"`{p}daily`")

        await ctx.send(embed = em)

    # thelp weekly
    @help.command()
    async def weekly(self, ctx):
        p = self.client.serverprefix
        em = discord.Embed(title = "Weekly",
                           description = "Receive your weekly reward",
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())
        em.add_field(name="**Syntax**",value=f"`{p}weekly`")

        await ctx.send(embed = em)

    # thelp monthly
    @help.command()
    async def monthly(self, ctx):
        p = self.client.serverprefix
        em = discord.Embed(title = "Monthly",
                           description = "Receive your monthly reward",
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())
        em.add_field(name="**Syntax**",value=f"`{p}monthly`")

        await ctx.send(embed = em)

    # thelp work
    @help.command()
    async def work(self, ctx):
        p = self.client.serverprefix
        em = discord.Embed(title = "Work",
                           description = "Convert your lifespan into cash.",
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())
        em.add_field(name="**Syntax**",value=f"`{p}work <occupation> <times>`")

        await ctx.send(embed = em)

    # thelp steal
    @help.command(aliases=['rob'])
    async def steal(self, ctx):
        p = self.client.serverprefix
        em = discord.Embed(title = "Steal",
                           description = "Steal someone's life savings",
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())
        em.add_field(name="**Syntax**",value=f"`{p}steal <user>`")
        em.add_field(name="**Aliases**",value=f"`{p}steal`, `{p}rob`")

        await ctx.send(embed = em)
    
    # thelp give
    @help.command()
    async def give(self, ctx):
        p = self.client.serverprefix
        em = discord.Embed(title = "Give",
                           description = "Give someone some of your life savings",
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())
        em.add_field(name="**Syntax**",value=f"`{p}give <user> <amount>`")

        await ctx.send(embed = em)

#####################################################################################################################################
############################################################# M U S I C #############################################################
########################################################### C O M A N D S ###########################################################
#####################################################################################################################################

    # thelp play
    @help.command(aliases=['sing'])
    async def play(self, ctx):
        p = self.client.serverprefix
        em = discord.Embed(title = "Play",
                           description = "Plays music from a url or tries to find the song on youtube.",
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())
        em.add_field(name="**Syntax**",value=f"`{p}play <audio>`")
        em.add_field(name="**Aliases**",value=f"`{p}play`, `{p}sing`")

        await ctx.send(embed = em)

    # thelp pause
    @help.command(aliases=['stop'])
    async def pause(self, ctx):
        p = self.client.serverprefix
        em = discord.Embed(title = "Pause",
                           description = "Pauses the music being played",
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())
        em.add_field(name="**Syntax**",value=f"`{p}pause`")
        em.add_field(name="**Aliases**",value=f"`{p}pause`, `{p}stop`")

        await ctx.send(embed = em)

    # thelp resume
    @help.command()
    async def resume(self, ctx):
        p = self.client.serverprefix
        em = discord.Embed(title = "Resume",
                           description = "Resumes playing music",
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())
        em.add_field(name="**Syntax**",value=f"`{p}resume`")

        await ctx.send(embed = em)

    # thelp leave
    @help.command(aliases=['disconnect'])
    async def leave(self, ctx):
        p = self.client.serverprefix
        em = discord.Embed(title = "Leave",
                           description = "Leaves the voice call",
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())
        em.add_field(name="**Syntax**",value=f"`{p}leave`")
        em.add_field(name="**Aliases**",value=f"`{p}leave`, `{p}disconnect`")

        await ctx.send(embed = em)
    
    # thelp join
    @help.command(aliases=['connect'])
    async def join(self, ctx):
        p = self.client.serverprefix
        em = discord.Embed(title = "Join",
                           description = "Joins the voice call",
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())
        em.add_field(name="**Syntax**",value=f"`{p}join`")
        em.add_field(name="**Aliases**",value=f"`{p}join`, `{p}connect`")

        await ctx.send(embed = em)

#####################################################################################################################################
######################################################## M O D E R A T I O N ########################################################
########################################################### C O M A N D S ###########################################################
#####################################################################################################################################

    # thelp purge
    @help.command(aliases=['clear'])
    async def purge(self, ctx):
        p = self.client.serverprefix
        em = discord.Embed(title = "Purge",
                           description = "Deletes a set ammount of messages from the channel",
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())
        em.add_field(name="**Syntax**",value=f"`{p}purge <ammount>`")
        em.add_field(name="**Aliases**",value=f"`{p}purge`, `{p}clear`")

        await ctx.send(embed = em)

    # thelp giveadmin
    @help.command()
    async def giveadmin(self, ctx):
        p = self.client.serverprefix
        em = discord.Embed(title = "Give admin",
                           description = "Gives a user admin. \n Usefull if someone doesnt know how to make and give someone an admin role.",
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())
        em.add_field(name="**Syntax**",value=f"`{p}giveadmin <user>`")

        await ctx.send(embed = em)

    # thelp kick
    @help.command()
    async def kick(self, ctx):
        p = self.client.serverprefix
        em = discord.Embed(title = "Kick",
                           description = "kicks an user.",
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())
        em.add_field(name="**Syntax**",value=f"`{p}kick <user> <reason>`")

        await ctx.send(embed = em)

    # thelp ban
    @help.command()
    async def ban(self, ctx):
        p = self.client.serverprefix
        em = discord.Embed(title = "Ban Hammer",
                           description = "Bans an user.",
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())
        em.add_field(name="**Syntax**",value=f"`{p}ban <user> <reason> <delete_messages_days>`")

        await ctx.send(embed = em)

    # thelp unban
    @help.command()
    async def unban(self, ctx):
        p = self.client.serverprefix
        em = discord.Embed(title = "unban Hammer?",
                           description = "unbans a user.",
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())
        em.add_field(name="**Syntax**",value=f"`{p}unban <user.id>`")

        await ctx.send(embed = em)

#####################################################################################################################################
######################################################## I N F O R M A T I O N ######################################################
########################################################### C O M A N D S ###########################################################
#####################################################################################################################################
    # thelp prefix
    @help.command()
    async def prefix(self, ctx):
        p = self.client.serverprefix
        em = discord.Embed(title = "Prefix",
                           description = "Returns the prefix for the server.",
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())
        em.add_field(name="**Syntax**",value=f"`{p}prefix`")

        await ctx.send(embed = em)
    
    # thelp ping
    @help.command()
    async def ping(self, ctx):
        p = self.client.serverprefix
        em = discord.Embed(title = "Ping",
                           description = "Tests bot's ping.",
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())

        em.add_field(name="**Syntax**",value=f"`{p}ping`")

        await ctx.send(embed = em)

    # thelp invite
    @help.command()
    async def invite(self, ctx):
        p = self.client.serverprefix
        em = discord.Embed(title = "Invite links",
                           description = "Returns a link for the bot, its support server, and some other links",
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())

        em.add_field(name="**Syntax**",value=f"`{p}invite`")

        await ctx.send(embed = em)

    # thelp upvote
    @help.command(aliases=['vote'])
    async def upvote(self, ctx):
        p = self.client.serverprefix
        em = discord.Embed(title = "Upvote TimelyBot",
                           description = "Gives you the link to upvote the bot in exchange for cool rewards",
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())
        em.add_field(name="**Syntax**",value=f"`{p}upvote`")
        em.add_field(name="**Aliases**",value=f"`{p}upvote`, `{p}vote`")

        await ctx.send(embed = em)

    # thelp creator
    @help.command()
    async def creator(self, ctx):
        p = self.client.serverprefix
        em = discord.Embed(title = "Zseni#5848",
                           description = "Returns some relevant information about my creator",
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())
        em.add_field(name="**Syntax**",value=f"`{p}creator`")
        em.add_field(name="**Aliases**",value=f"`{p}zseni`, `{p}genius`, `{p}creator`")

        await ctx.send(embed = em)

    # thelp developers
    @help.command()
    async def developers(self, ctx):
        p = self.client.serverprefix
        em = discord.Embed(title = "Developers",
                           description = f"Returns a list of users working on {self.client.user.mention}",
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())
        em.add_field(name="**Syntax**",value=f"`{p}developers`")

        await ctx.send(embed = em)
    
    # thelp userinfo
    @help.command(aliases=['ui'])
    async def userinfo(self, ctx):
        p = self.client.serverprefix
        em = discord.Embed(title = "User's Information",
                           description = "Returns a user's basic information",
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())

        em.add_field(name="**Syntax**",value=f"`{p}userinfo <users>`")
        em.add_field(name="**Aliases**",value=f"`{p}userinfo`, `{p}ui`")

        await ctx.send(embed = em)

    # thelp serverinfo
    @help.command(aliases=['si'])
    async def serverinfo(self, ctx):
        p = self.client.serverprefix
        em = discord.Embed(title = "Server's Information",
                           description = "Returns the server's basic information",
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())

        em.add_field(name="**Syntax**",value=f"`{p}serverinfo <users>`")
        em.add_field(name="**Aliases**",value=f"`{p}serverinfo`, `{p}si`")

        await ctx.send(embed = em)

    # thelp avatar
    @help.command()
    async def avatar(self, ctx):
        p = self.client.serverprefix
        em = discord.Embed(title = "Avatar",
                           description = "Returns a users avatar.",
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())
        em.add_field(name="**Syntax**",value=f"`{p}avatar <user>`")

        await ctx.send(embed = em)

    # thelp botinfo
    @help.command()
    async def botinfo(self, ctx):
        p = self.client.serverprefix
        em = discord.Embed(title = "BotInfo",
                           description = "Returns general and system information on the bot.",
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())
        em.add_field(name="**Syntax**",value=f"`{p}botinfo`")

        await ctx.send(embed = em)

    # thelp oldest
    @help.command()
    async def oldest(self, ctx):
        p = self.client.serverprefix
        em = discord.Embed(title = "Oldest",
                           description = "Returns the oldest accounts in the server.",
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())
        em.add_field(name="**Syntax**",value=f"`{p}oldest`")

        await ctx.send(embed = em)
    
    # thelp newest
    @help.command()
    async def newest(self, ctx):
        p = self.client.serverprefix
        em = discord.Embed(title = "Newest",
                           description = "Returns the newest accounts in the server.",
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())
        em.add_field(name="**Syntax**",value=f"`{p}newest`")

        await ctx.send(embed = em)

#####################################################################################################################################
########################################################## S E T T I N G S ##########################################################
########################################################### C O M A N D S ###########################################################
#####################################################################################################################################

    # thelp changeprefix
    @help.command()
    async def changeprefix(self, ctx):
        p = self.client.serverprefix
        em = discord.Embed(title = "Change Prefix",
                           description = "changes the prefx for the server.",
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())

        em.add_field(name="**Syntax**",value=f"`{p}changeprefix <newprefix>`")

        await ctx.send(embed = em)


#####################################################################################################################################
def setup(client):
    client.add_cog(help(client))
