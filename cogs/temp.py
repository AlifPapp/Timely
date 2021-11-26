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
        try: 
            if not ctx.author.bot: return True
        except: pass

    # thelp
    @commands.group(invoke_without_command=True)
    async def help(self, ctx):
        return
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
        em.add_field(name="**Syntax**",value=f"`{p}balance [user]`")
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
        em.add_field(name="**Syntax**",value=f"`{p}profile [user]`")

        await ctx.send(embed = em)

    # thelp rich
    @help.command()
    async def rich(self, ctx):
        p = self.client.serverprefix
        em = discord.Embed(title = "Rich",
                           description = "Returns the richest users in the server",
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())
        em.add_field(name="**Syntax**",value=f"`{p}rich [page]`")
        
        await ctx.send(embed = em)

    # thelp globalrich
    @help.command()
    async def globalrich(self, ctx):
        p = self.client.serverprefix
        em = discord.Embed(title = "Global Rich",
                           description = "Returns the richest users in Timely",
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())
        em.add_field(name="**Syntax**",value=f"`{p}globalrich [page]`")
        
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
        em.add_field(name="**Syntax**",value=f"`{p}work <occupation> [times]`")
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
        em.add_field(name="**Syntax**",value=f"`{p}pray [user]`")
        em.add_field(name="**Values**",value=f"Cooldown: 30 Seconds\nEarnings: 1-24 hours",inline = False)

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

        em.add_field(name="**Syntax**",value=f"`{p}serverinfo [users]`")
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
        em.add_field(name="**Syntax**",value=f"`{p}serveremojis [page]`")
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
        em.add_field(name="**Syntax**",value=f"`{p}oldest [page]`")

        await ctx.send(embed = em)
    
    # thelp newest
    @help.command()
    async def newest(self, ctx):
        p = self.client.serverprefix
        em = discord.Embed(title = "Newest",
                           description = "Returns the newest accounts in the server.",
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())
        em.add_field(name="**Syntax**",value=f"`{p}newest [page]`")

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

        em.add_field(name="**Syntax**",value=f"`{p}userinfo [users]`")
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
        em.add_field(name="**Syntax**",value=f"`{p}avatar [user]`")
        em.add_field(name="**Aliases**",value=f"`{p}avatar`, `{p}av`")

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
############################################################ R E D D I T ############################################################
########################################################### C O M A N D S ###########################################################
#####################################################################################################################################

    # thelp redditsearch
    @help.command()
    async def redditsearch(self, ctx):
        p = self.client.serverprefix
        em = discord.Embed(title = "redditsearch",
                           description = "Returns submissions from a subreddit.",
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())

        em.add_field(name="**Syntax**",value=f"`{p}redditsearch r/<subreddit>`")

        await ctx.send(embed = em)
    
    # thelp redditleaderboard
    @help.command()
    async def redditleaderboard(self, ctx):
        p = self.client.serverprefix
        em = discord.Embed(title = "redditleaderboard",
                           description = "Returns the most used subreddit in timely.",
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())

        em.add_field(name="**Syntax**",value=f"`{p}redditleaderboard [all/month/week/now] [page]`")

        await ctx.send(embed = em)


#####################################################################################################################################
def setup(client):
    client.add_cog(help(client))
