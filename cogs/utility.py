import discord 
from discord.ext import commands

from datetime import datetime
from typing import Optional

from discord import Embed, Member

import psutil

class other(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("other.py Loaded!")

    async def cog_check(self, ctx):
        if ctx.guild is not None: return True
        if not ctx.author.bot: return True

    # tinvite
    @commands.command()
    async def invite(self, ctx):
        em = discord.Embed(title = "",
                           description = "",
                           colour = self.client.Blue,
                           timestamp=datetime.utcnow())

        em.add_field(name= "**Add TimelyBot**", value = "[here](https://discord.com/api/oauth2/authorize?client_id=836198930873057290&permissions=8&scope=bot)", inline=True)
        em.add_field(name= "**SupportServer**", value = "[here](https://discord.gg/E8DnTgMvMW)", inline=True)

        await ctx.send(embed = em)

    # tupvote
    @commands.command(aliases=['vote'])
    async def upvote(self, ctx):
        em = discord.Embed(title = "Upvote TimelyBot",
                           description = "",
                           colour = self.client.Blue,
                           timestamp=datetime.utcnow())
        em.set_thumbnail(url="https://emoji.gg/assets/emoji/BirdUpvote.gif")

        em.add_field(name= "__discordbotlist.com__", value = "[Upvote](https://discord.ly/timely-3816)", inline=False)
        em.add_field(name= "__voidbots.net__", value = "[Upvote](https://voidbots.net/bot/836198930873057290/)", inline=False)
        em.add_field(name= "Rewards", value = "-Luck +10%\n-Baby's blood x1", inline=False)

        await ctx.send(embed = em)

    # tzseni
    @commands.command(aliases=['genius','zseni'])
    async def creator(self, ctx):
        em = discord.Embed(title = "Zseni#5848 is my creator.",
                           description = "Special thanx to MinuteLad#6546 for the basic idea and art.",
                           colour = self.client.Blue,
                           timestamp=datetime.utcnow())
        em.set_thumbnail(url="https://imgur.com/wSnPFbH.gif")

        em.add_field(name= "Youtube", value = "[here](http://bit.ly/Zseni-Youtube )", inline=True)
        em.add_field(name= "Discord", value = "[here](https://discord.gg/SXng95f)", inline=True)
        em.add_field(name= "Twitter", value = "[here](https://twitter.com/Zseni10)", inline=True)

        await ctx.send(embed = em)
    
    # ping pong (test latency)
    @commands.command()
    async def ping(self, ctx):
        em = discord.Embed(title = "<a:pingpongparrot:849455355222425630>Pong!",
                           description = f"Latency: {round(self.client.latency * 1000)}ms",
                           colour = self.client.Blue)
        t = await ctx.send(embed = em)

    # tuserinfo <user>(optional)
    @commands.command(aliases=['ui'])
    async def userinfo(self, ctx, target: Optional[Member]):
        target = target or ctx.author

        em = Embed(title=f"User Info - {target}",
                   description=target.mention,
                   colour=self.client.Blue)
        em.set_thumbnail(url=target.avatar_url)

        roles_string = []
        perms_string = []
        perms_string_allperms = "Manage Channels, Manage Emojis, Manage Server, Manage Messages, Manage Nicknames, Manage Roles, Manage Webhooks, Kick Members, Ban Members, Mention Everyone"
        Acknowledgement = None
        #Search for roles and its perms
        for role in target.roles:
            if role.name != "@everyone":
                roles_string.append(role.mention)
            
            for perm, true_false in role.permissions:
                if true_false is True:
                    #Check if have adminsitrator perms and if checked before
                    if perm == "administrator":
                        if "Administrator" not in perms_string:
                            Acknowledgement = "Server Admin"
                    #Check for Key permissions through function
                    check = await check_user_keypermissions(perm,perms_string)
                    if check != None:
                        perms_string.append(check)
        
        #Check if have roles.
        roles_lenght = len(target.roles) - 1
        if roles_lenght == 0:
            roles_string = "None"
        else:
            roles_string = ", ".join(roles_string)

        join_pos = sum(m.joined_at < target.joined_at for m in ctx.guild.members if m.joined_at is not None) + 1
        creation_pos = sum(m.created_at < target.created_at for m in ctx.guild.members if m.created_at is not None) + 1
        fields = [(f"Joined[{join_pos}/{len(ctx.guild.members)}]", target.joined_at.strftime("%a, %b %d %Y %I:%M %p"), True),
                  (f"Created[{creation_pos}/{len(ctx.guild.members)}]", target.created_at.strftime("%a, %b %d %Y %I:%M %p"), True),
                  (f"Roles[{roles_lenght}]",roles_string, False)]
        
        #Check if Server Owner or Server Admin. if so give allperms. if not but have perms append Key Permissions
        perms_lenght = len(perms_string)
        if ctx.guild.owner == target or Acknowledgement == "Server Admin":
            perms_string = perms_string_allperms
            fields.append(("Key Permissions", perms_string, False))
        else:
            if perms_lenght != 0:
                perms_string = ", ".join(perms_string)
                fields.append(("Key Permissions", perms_string, False))

        #Check if Server Owner or Server Admin. If so give Acknowledgement
        if Acknowledgement == "Server Admin":
            fields.append(("Acknowledgements", Acknowledgement, False))
        if ctx.guild.owner == target:
            Acknowledgement = "Server Owner"
            fields.append(("Acknowledgements", Acknowledgement, False))


        for name, value, inline in fields:
        	em.add_field(name=name, value=value, inline=inline)

        em.set_footer(text=f"ID: {ctx.author.id}")
        em.timestamp = datetime.utcnow()

        await ctx.reply(embed = em)

    # tserverinfo
    @commands.command(aliases=["si"])
    async def serverinfo(self, ctx):
        em = Embed(title=f"Server Info - {ctx.guild.name}",
                  colour=self.client.Blue)
                
        em.set_thumbnail(url=ctx.guild.icon_url)

        statuses = [len(list(filter(lambda m: str(m.status) == "online", ctx.guild.members))),
                    len(list(filter(lambda m: str(m.status) == "idle", ctx.guild.members))),
                    len(list(filter(lambda m: str(m.status) == "dnd", ctx.guild.members))),
                    len(list(filter(lambda m: str(m.status) == "offline", ctx.guild.members)))]

        Members = [len(ctx.guild.members),
                   len(list(filter(lambda m: not m.bot, ctx.guild.members))),
                   len(list(filter(lambda m: m.bot, ctx.guild.members))),
                   len(await ctx.guild.bans())]

        Channels = [len(ctx.guild.text_channels),
                    len(ctx.guild.voice_channels),
                    len(ctx.guild.categories)]

        Info = [ctx.guild.owner,
                ctx.guild.created_at.strftime("%d/%m/%Y"),
                ctx.guild.region,
                len(ctx.guild.roles)]

        fields = [("Info",f"Owner: {Info[0]}\nCreated: {Info[1]}\nVoice region: {Info[2]}\nRoles: {Info[3]}",True),
                  ("Channels", f"<:text_channel:846217104381575238> {Channels[0]}\n<:voice_channel:846217088535494707> {Channels[1]}\n<:category:846219026123849749> {Channels[2]}", True),
                  ("Members", f"Total: {Members[0]}\nHumans: {Members[1]}\nBots: {Members[2]}\nBanned: {Members[3]}", True),
                  ("Statuses", f"<:online_status:847720675866705941>{statuses[0]} <:idle_status:847720792299929620>{statuses[1]} <:dnd_status:847720837654249512> {statuses[2]}<:offline_status:847720744288256031> {statuses[3]}", True),
                  ("\u200b", "\u200b", True)]

        for name, value, inline in fields:
            em.add_field(name=name, value=value, inline=inline)

        em.set_footer(text=f"ID: {ctx.guild.id}")
        em.timestamp = datetime.utcnow()

        await ctx.reply(embed = em)

    # tbotinfo
    @commands.command()
    async def botinfo(self, ctx):
        memory_total = psutil.virtual_memory()._asdict()["total"]
        memory_used = psutil.virtual_memory()._asdict()["used"]
        memory_percent = psutil.virtual_memory()._asdict()["percent"]
        cpu_percent = psutil.cpu_percent()

        users_sum = 0
        for x in self.client.guilds:
            users_sum += len(x.members)

        em = Embed(title=f"Bot Info - {self.client.user}",
                  colour=self.client.Blue)
        em.set_thumbnail(url=self.client.user.avatar_url)

        Vars = ["<@!416508283528937472>",
                self.client.user.created_at.strftime("%d/%m/%Y"),
                len(self.client.guilds),
                f"{int(memory_used/1000000)}/{int(memory_total/1000000)} ({memory_percent}%)",
                f"[discord.py](https://discordpy.readthedocs.io/en/latest/) {discord.__version__}",
                f"[MongoDB](https://www.mongodb.com/)",
                f"[Heroku](https://dashboard.heroku.com/)"]

        fields = [("Info",f"Owner: {Vars[0]}\nCreated: {Vars[1]}\nGuilds: {Vars[2]}\nUsers: {users_sum}",False),
                  ("System",f"CPU: {cpu_percent}%\nMemory: {Vars[3]}\nFramework: {Vars[4]}\nDataBase: {Vars[5]}\nHosted on: {Vars[6]}",True)]

        for name, value, inline in fields:
            em.add_field(name=name, value=value, inline=inline)

        em.set_footer(text=f"ID: {self.client.user.id}")
        em.timestamp = datetime.utcnow()
        await ctx.reply(embed = em)

    # toldest
    @commands.command()
    async def oldest(self, ctx, page: int=1):
        await oldest_newest(self, ctx, page, "Oldest")
    # tnewest
    @commands.command()
    async def newest(self, ctx, page: int=1):
        await oldest_newest(self, ctx, page, "Newest")

async def oldest_newest(self, ctx, page, sort_type):
    page = abs(int(page))
    if page > 99: page = 99
    
    x1 = x2 = x3 = x4 = x5 = x6 = x7 = x8 = x9 = x10 = None
    searchint = (page-1)*10
    for x in ctx.guild.members:
        if sort_type == "Oldest": creation_pos = sum(m.created_at < x.created_at for m in ctx.guild.members if m.created_at is not None) + 1
        if sort_type == "Newest": creation_pos = sum(m.created_at > x.created_at for m in ctx.guild.members if m.created_at is not None) + 1
        if creation_pos == searchint+1: x1 = x
        if creation_pos == searchint+2: x2 = x
        if creation_pos == searchint+3: x3 = x
        if creation_pos == searchint+4: x4 = x
        if creation_pos == searchint+5: x5 = x
        if creation_pos == searchint+6: x6 = x
        if creation_pos == searchint+7: x7 = x
        if creation_pos == searchint+8: x8 = x
        if creation_pos == searchint+9: x9 = x
        if creation_pos == searchint+10: x10 = x 
    
    members_sorted =[]
    if x1 is not None: members_sorted.append(x1)
    if x2 is not None: members_sorted.append(x2)
    if x3 is not None: members_sorted.append(x3)
    if x4 is not None: members_sorted.append(x4)
    if x5 is not None: members_sorted.append(x5)
    if x6 is not None: members_sorted.append(x6)
    if x7 is not None: members_sorted.append(x7)
    if x8 is not None: members_sorted.append(x8)
    if x9 is not None: members_sorted.append(x9)
    if x10 is not None: members_sorted.append(x10)

    cycle_int = 0
    output_string = ""
    for x in members_sorted:
        cycle_int = cycle_int + 1
        output_string += f"**{cycle_int+((page-1)*10)}** - {x} - {x.created_at.strftime('%d/%m/%Y')}\n"

    em = discord.Embed(color=self.client.Blue)
    em.add_field(name=f"{sort_type} accounts in **{ctx.guild.name}**", value=output_string, inline=False)

    em.set_footer(text=f"Page: {page}")
    em.timestamp = datetime.utcnow()
        
    await ctx.send(embed=em)

async def check_user_keypermissions(perm,perms_string):
    if perm == "manage_channels":
        if "Manage Channels" not in perms_string:
            return "Manage Channels"
    
    if perm == "manage_emojis":
        if "Manage Emojis" not in perms_string:
            return "Manage Emojis"
    
    if perm == "manage_guild":
        if "Manage Server" not in perms_string:
            return "Manage Server"

    if perm == "manage_messages":
        if "Manage Messages" not in perms_string:
            return "Manage Messages"

    if perm == "manage_nicknames":
        if "Manage Nicknames" not in perms_string:
            return "Manage Nicknames"

    if perm == "manage_roles":
        if "Manage Roles" not in perms_string:
            return "Manage Roles"
    
    if perm == "manage_webhooks":
        if "Manage Webhooks" not in perms_string:
            return "Manage Webhooks"

    if perm == "kick_members":
        if "Kick Members" not in perms_string:
            return "Kick Members"

    if perm == "ban_members":
        if "Ban Members" not in perms_string:
            return "Ban Members"

    if perm == "mention_everyone":
        if "Mention Everyone" not in perms_string:
            return "Mention Everyone"
    return None


#####################################################################################################################################
def setup(client):
    client.add_cog(other(client))