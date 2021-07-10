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
                           description = f"**Prefix:** `{p}` and {self.client.user.mention}\nIf you have any questions/queries feel free to join the [support server](https://discord.gg/E8DnTgMvMW)",
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())

        em.add_field(name="<:coin:862881131799248937> Currency",value=f"`{p}help currency`",inline=True)
        em.add_field(name="<a:music:862881551780282368> Music",value = f"`{p}help music`",inline=True)
        em.add_field(name="<:info:862881844265746442> Information",value = f"`{p}help information`",inline=True)
        em.add_field(name="<:count:862882885916033054> Counting",value = f"`{p}help counting`",inline=True)
        em.add_field(name="<:moderator:862883498214162453> Moderation",value = f"`{p}help moderation`",inline=True)
        em.add_field(name="<:static_cog:862507223062151168> Settings",value = f"`{p}help settings`",inline=True)
        await ctx.send(embed = em)


    # thelp Currency
    @help.command()
    async def currency(self, ctx):
        p = self.client.serverprefix

        commands_list = sorted(["balance","profile","rich","globalrich",
                         "daily","weekly","monthly",
                         "card","slots",
                         "pray","work","steal","give"])
        commands_list = f"`, `{p}".join(commands_list)
        commands_list = f"`{p}{commands_list}`"

        em = discord.Embed(title = "<:coin:862881131799248937> Currency commands",
                           description = commands_list,
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())

        em.set_footer(text=f"{p}help <command>")
        await ctx.send(embed = em)

    # thelp devCurrency
    @help.command()
    async def devcurrency(self, ctx):
        p = self.client.serverprefix

        commands_list = sorted(["editusercurrency","openaccountcurrency"])
        commands_list = f"`, `{p}".join(commands_list)
        commands_list = f"`{p}{commands_list}`"

        em = discord.Embed(title = "<:coin:862881131799248937> Currency Moderator commands",
                           description = commands_list,
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())

        em.set_footer(text=f"{p}help <command>")
        await ctx.send(embed = em)

    # thelp Music
    @help.command()
    async def music(self, ctx):
        p = self.client.serverprefix

        commands_list = sorted(["play","pause","resume","leave","join"])
        commands_list = f"`, `{p}".join(commands_list)
        commands_list = f"`{p}{commands_list}`"

        em = discord.Embed(title = "<a:music:862881551780282368> Music commands",
                           description = commands_list,
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())

        em.set_footer(text=f"{p}help <command>")
        await ctx.send(embed = em)

    # thelp Information
    @help.command()
    async def information(self, ctx):
        p = self.client.serverprefix

        commands_list = sorted(["prefix","ping","invite","developers","botinfo",
                                "serverinfo","serveremojis","serveravatar","oldest","newest",
                                "userinfo","avatar"])
        commands_list = f"`, `{p}".join(commands_list)
        commands_list = f"`{p}{commands_list}`"

        em = discord.Embed(title = "<:info:862881844265746442> Informational commands",
                           description = commands_list,
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())

        em.set_footer(text=f"{p}help <command>")
        await ctx.send(embed = em)

    # thelp counting
    @help.command()
    async def counting(self, ctx):
        p = self.client.serverprefix
        
        commands_list = sorted(["setupcounting"])
        commands_list = f"`, `{p}".join(commands_list)
        commands_list = f"`{p}{commands_list}`"

        em = discord.Embed(title = "<:count:862882885916033054> Counting commands",
                           description = commands_list,
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())

        em.set_footer(text=f"{p}help <command>")
        await ctx.send(embed = em)

    # thelp Moderation
    @help.command()
    async def moderation(self, ctx):
        p = self.client.serverprefix

        commands_list = sorted(["purge","giveadmin","kick","ban","unban"])
        commands_list = f"`, `{p}".join(commands_list)
        commands_list = f"`{p}{commands_list}`"

        em = discord.Embed(title = "<:moderator:862883498214162453> Moderation commands",
                           description = commands_list,
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())

        em.set_footer(text=f"{p}help <command>")
        await ctx.send(embed = em)

    # thelp Settings
    @help.command()
    async def settings(self, ctx):
        p = self.client.serverprefix

        commands_list = sorted(["changeprefix"])
        commands_list = f"`, `{p}".join(commands_list)
        commands_list = f"`{p}{commands_list}`"

        em = discord.Embed(title = "<:static_cog:862507223062151168> Settings commands",
                           description = commands_list,
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())

        em.set_footer(text=f"{p}help <command>")
        await ctx.send(embed = em)


#####################################################################################################################################
########################################################## C U R R E N C Y ##########################################################
########################################################### C O M A N D S ###########################################################
#####################################################################################################################################

########################################################### Informational ###########################################################
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
        em.add_field(name="**Syntax**",value=f"`{p}rich <page>`")
        
        await ctx.send(embed = em)

    # thelp globalrich
    @help.command()
    async def globalrich(self, ctx):
        p = self.client.serverprefix
        em = discord.Embed(title = "Global Rich",
                           description = "Returns the richest users in Timely",
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())
        em.add_field(name="**Syntax**",value=f"`{p}globalrich <page>`")
        
        await ctx.send(embed = em)

############################################################# Periodic ##############################################################
    # thelp daily
    @help.command()
    async def daily(self, ctx):
        p = self.client.serverprefix
        em = discord.Embed(title = "Daily",
                           description = "Receive your daily reward",
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())
        em.add_field(name="**Syntax**",value=f"`{p}daily`")
        em.add_field(name="**Cooldown**",value=f"Cooldown: 24 hours\nEarnings: $250",inline = False)

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
        em.add_field(name="**Values**",value=f"Cooldown: 7 days\nEarnings: $750",inline = False)

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
        em.add_field(name="**Values**",value=f"Cooldown: 31 days\nEarnings: $2000",inline = False)
        
        await ctx.send(embed = em)

############################################################## Gamble ###############################################################
    # thelp card
    @help.command()
    async def card(self, ctx):
        p = self.client.serverprefix
        em = discord.Embed(title = "Card",
                           description = "Gamble your savings with another user",
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())
        em.add_field(name="**Syntax**",value=f"`{p}card <user> <ammount>`")
        em.add_field(name="**Values**",value=f"Cooldown: 5 Secconds",inline = False)

        await ctx.send(embed = em)

    # thelp slots
    @help.command()
    async def slots(self, ctx):
        p = self.client.serverprefix
        em = discord.Embed(title = "Slots",
                           description = "Use the Slot Machine to gamble your savings",
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())
        em.add_field(name="**Syntax**",value=f"`{p}slots <ammount>`")
        em.add_field(name="**Values**",value=f"Cooldown: 5 Secconds",inline = False)

        await ctx.send(embed = em)

############################################################### Earn ################################################################
    # thelp work
    @help.command()
    async def work(self, ctx):
        p = self.client.serverprefix
        em = discord.Embed(title = "Work",
                           description = "Convert your lifespan into savings.",
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())
        em.add_field(name="**Syntax**",value=f"`{p}work <occupation> <times>`")
        em.add_field(name="**Values**",value=f"Cooldown: 7 Seconds",inline = False)

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
        em.add_field(name="**Values**",value=f"Cooldown: 5 Minutes\nRequirements: $500\nSuccess Rate: 20%\nSteal over 50%: 5% chance\nPenalty: -5 Days",inline = False)

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
        em.add_field(name="**Values**",value=f"Cooldown: 7 Seconds",inline = False)

        await ctx.send(embed = em)

    # thelp pray
    @help.command()
    async def pray(self, ctx):
        p = self.client.serverprefix
        em = discord.Embed(title = "Pray",
                           description = "Beg God for good health",
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())
        em.add_field(name="**Syntax**",value=f"`{p}pray <user>`")
        em.add_field(name="**Values**",value=f"Cooldown: 30 Seconds\nEarnings: 1-24 hours",inline = False)

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
######################################################## I N F O R M A T I O N ######################################################
########################################################### C O M A N D S ###########################################################
#####################################################################################################################################

############################################################## Bot Info #############################################################
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
    
    # thelp botinfo
    @help.command()
    async def botinfo(self, ctx):
        p = self.client.serverprefix
        em = discord.Embed(title = "BotInfo",
                           description = "Returns general and system information on the bot.",
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())
        em.add_field(name="**Syntax**",value=f"`{p}botinfo`")
        em.add_field(name="**Aliases**",value=f"`{p}botinfo`, `{p}bi`")

        await ctx.send(embed = em)

############################################################# Server Info ###########################################################
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

    # thelp serveremojis
    @help.command(aliases=['se'])
    async def serveremojis(self, ctx):
        p = self.client.serverprefix
        em = discord.Embed(title = "Server Emojis",
                           description = "Returns a list of emojis in the current server.",
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())
        em.add_field(name="**Syntax**",value=f"`{p}serveremojis <page>`")
        em.add_field(name="**Aliases**",value=f"`{p}serveremojis`, `{p}se`")

        await ctx.send(embed = em)

    # thelp serveravatar
    @help.command(aliases=['sa'])
    async def serveravatar(self, ctx):
        p = self.client.serverprefix
        em = discord.Embed(title = "Server Avatar",
                           description = "Returns the servers avatar.",
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())
        em.add_field(name="**Syntax**",value=f"`{p}serveravatar`")
        em.add_field(name="**Aliases**",value=f"`{p}serveravatar`, `{p}sa`")

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

############################################################## User Info ############################################################
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

    # thelp avatar
    @help.command(aliases=['av'])
    async def avatar(self, ctx):
        p = self.client.serverprefix
        em = discord.Embed(title = "Avatar",
                           description = "Returns a users avatar.",
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())
        em.add_field(name="**Syntax**",value=f"`{p}avatar <user>`")
        em.add_field(name="**Aliases**",value=f"`{p}avatar`, `{p}av`")

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
############################################################# O T H E R #############################################################
########################################################### C O M A N D S ###########################################################
#####################################################################################################################################

    # thelp setupcounting
    @help.command()
    async def setupcounting(self, ctx):
        p = self.client.serverprefix
        em = discord.Embed(title = "Setup Counting",
                           description = "Setup a channel to be used for counting. The bot will replace the users message with a webhook version. This prevents users from editing their message or deleting it.",
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())

        em.add_field(name="**Syntax**",value=f"`{p}setupcounting`")

        await ctx.send(embed = em)

#####################################################################################################################################
def setup(client):
    client.add_cog(help(client))
