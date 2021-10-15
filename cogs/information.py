import discord
from discord.ext import commands

from datetime import datetime
from typing import Optional

from discord import Embed, Member

from .functions import basic_embed

import psutil

class information(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("other.py Loaded!")

    async def cog_check(self, ctx):
        try: 
            if ctx.guild is not None and not ctx.author.bot: return True
        except: pass

############################################################## Bot Info #############################################################
    # tinvite
    @commands.command()
    async def invite(self, ctx):
        em = discord.Embed(title = "",
                           description = "",
                           colour = self.client.Blue,
                           timestamp=datetime.utcnow())
        admin_invitelink = f"[admin_perms](https://discord.com/api/oauth2/authorize?client_id={self.client.user.id}&permissions=8&scope=bot%20applications.commands)"
        choice_invitelink = f"[choose_perms](https://discord.com/api/oauth2/authorize?client_id={self.client.user.id}&permissions=4294967287&scope=bot%20applications.commands)"
        em.add_field(name= "**Add TimelyBot**", value = f"{admin_invitelink}\n{choice_invitelink}", inline=False)
        em.add_field(name= "**SupportServer**", value = "[here](https://discord.gg/E8DnTgMvMW)", inline=False)

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
    
    # ping pong (test latency)
    @commands.command()
    async def ping(self, ctx):
        em = discord.Embed(title = "<a:pingpongparrot:849455355222425630>Pong!",
                           description = f"Latency: {round(self.client.latency * 1000)}ms",
                           colour = self.client.Blue)
        t = await ctx.send(embed = em)

    # tbotinfo
    @commands.command(aliases=['bi'])
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
        em.set_thumbnail(url=self.client.user.avatar.url)

        Vars = ["<@!416508283528937472>",
                self.client.user.created_at.strftime("%d/%m/%Y"),
                len(self.client.guilds),
                f"{int(memory_used/1000000)}/{int(memory_total/1000000)} MB ({memory_percent}%)",
                f"[discord.py](https://discordpy.readthedocs.io/en/latest/) {discord.__version__}",
                f"[MongoDB](https://www.mongodb.com/)",
                f"[Heroku](https://dashboard.heroku.com/)"]

        fields = [("<:folder:874116455409528904> Info",f"Owner: {Vars[0]}\nCreated: {Vars[1]}\nGuilds: {Vars[2]}\nUsers: {users_sum}",False),
                  (":file_cabinet:System",f"CPU: {cpu_percent}%\nMemory: {Vars[3]}\nFramework: {Vars[4]}\nDataBase: {Vars[5]}\nHosted on: {Vars[6]}",True)]

        for name, value, inline in fields:
            em.add_field(name=name, value=value, inline=inline)

        em.set_footer(text=f"ID: {self.client.user.id}")
        em.timestamp = datetime.utcnow()
        await ctx.reply(embed = em)

############################################################## User Info ############################################################
    # tuserinfo <user>(optional)
    @commands.command(aliases=['ui'])
    async def userinfo(self, ctx, target: Optional[Member]):
        target = target or ctx.author
        try: target_avatar_url = target.avatar.url
        except: target_avatar_url = ""

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
        fields = [(f"Joined [{join_pos}/{len(ctx.guild.members)}]", target.joined_at.strftime("%a, %b %d %Y %I:%M %p"), True),
                  (f"Created [{creation_pos}/{len(ctx.guild.members)}]", target.created_at.strftime("%a, %b %d %Y %I:%M %p"), True),
                  (f"Roles [{roles_lenght}]",roles_string, False)]
        
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

        #Find what platform target is using
        status_string = ""
        if target.desktop_status == discord.Status.online: status_string += "<:desktop_online:862217464381177866>"
        if target.desktop_status == discord.Status.idle: status_string += "<:desktop_idle:862217516976701499>"
        if target.desktop_status == discord.Status.dnd: status_string += "<:desktop_dnd:862217565974429726>"

        if target.mobile_status == discord.Status.online: status_string += "<:mobile_online:862217637794545675>"
        if target.mobile_status == discord.Status.idle: status_string += "<:mobile_idle:862217700301864960>"
        if target.mobile_status == discord.Status.dnd: status_string += "<:mobile_dnd:862217743082979329>"

        if target.web_status == discord.Status.online: status_string += "<:browser_online:862217876797390860>"
        if target.web_status == discord.Status.idle: status_string += "<:browser_idle:862217926487834624>"
        if target.web_status == discord.Status.dnd: status_string += "<:browser_dnd:862217975603789844>"

        if status_string == "": status_string = "NA"

        em = Embed(title=f"User Info - {target}",
                   description=f"{target.mention} [{status_string}]",
                   colour=self.client.Blue)
        em.set_thumbnail(url=target_avatar_url)

        for name, value, inline in fields:
        	em.add_field(name=name, value=value, inline=inline)

        em.set_footer(text=f"ID: {ctx.author.id}")
        em.timestamp = datetime.utcnow()

        await ctx.reply(embed = em)

    # tavatar
    @commands.command(aliases=['av'])
    async def avatar(self, ctx, target: Optional[Member]):
        target = target or ctx.author
        try: target_avatar_url = target.avatar.url
        except: target_avatar_url = ""
        
        em = Embed(title=f"",
                   description=f"",
                   colour=self.client.Blue)
        
        em.set_author(name=f"{target}'s Avatar", icon_url = target_avatar_url)

        em.set_image(url=target_avatar_url)
        em.set_footer(text=f"ID: {target.id}")
        em.timestamp = datetime.utcnow()

        await ctx.reply(embed = em)

############################################################# Server Info ###########################################################
    # tserverinfo
    @commands.command(aliases=["si"])
    async def serverinfo(self, ctx):
        em = Embed(title=f"",
                  colour=self.client.Blue)
        try: guild_icon_url = ctx.guild.icon.url
        except: guild_icon_url = ""
                
        em.set_thumbnail(url=guild_icon_url)
        em.set_author(name=f"{ctx.guild.name} | Server Info", icon_url = guild_icon_url)

        #Channels
        locked_channel = len([i for i in ctx.guild.text_channels if i.overwrites_for(ctx.guild.default_role).send_messages == False])
        if locked_channel != 0: locked_channel = f" locked ({locked_channel})"
        else: locked_channel = " "

        locked_voice = len([i for i in ctx.guild.voice_channels if i.overwrites_for(ctx.guild.default_role).connect == False])
        if locked_voice != 0: locked_voice = f" locked ({locked_voice})"
        else: locked_voice = " "

        Channels = [f"<:announcements:862203838375395338> {len([i for i in ctx.guild.channels if str(i.type) == 'news'])}",
                    f"<:stage:862200069783289856> {len(ctx.guild.stage_channels)}",
                    f"<:category:862208265244114974> {len(ctx.guild.categories)}",
                    f"<:text_channel:862208150336569364> {len(ctx.guild.text_channels)} {locked_channel}",
                    f"<:voice_channel:862208215117594662> {len(ctx.guild.voice_channels)} {locked_voice}"]

        #Members
        Members = [len(ctx.guild.members),
                   len(list(filter(lambda m: not m.bot, ctx.guild.members))),
                   len(list(filter(lambda m: m.bot, ctx.guild.members)))]

        try:
            guild_bans_lenght = len(await ctx.guild.bans())
        except discord.Forbidden:
            guild_bans_lenght = f"MissingPerms"
        
        #Emojis
        animated_emojis = 0
        for x in ctx.guild.emojis:
            if x.animated:
                animated_emojis = animated_emojis + 1

        emojis =[f"{(len(ctx.guild.emojis)-animated_emojis)}/{ctx.guild.emoji_limit}",
                 f"{animated_emojis}/{ctx.guild.emoji_limit}",
                 f"{len(ctx.guild.emojis)}/{ctx.guild.emoji_limit*2}"]

        #Status
        statuses = [len(list(filter(lambda m: str(m.status) == "online", ctx.guild.members))),
                    len(list(filter(lambda m: str(m.status) == "idle", ctx.guild.members))),
                    len(list(filter(lambda m: str(m.status) == "dnd", ctx.guild.members))),
                    len(list(filter(lambda m: str(m.status) == "offline", ctx.guild.members)))]

        online_status_emoji = "<:online_status:863387938439299072>"
        idle_status_emoji = "<:idle_status:863387977782788117>"
        dnd_status_emoji = "<:dnd_status:863388021877243934>"
        offline_status_emoji = "<:offline_status:863388067691888651>"
        
        if str(ctx.guild.verification_level) == "none": verification_level = 0
        if str(ctx.guild.verification_level) == "low": verification_level = 1 
        if str(ctx.guild.verification_level) == "medium": verification_level = 2
        if str(ctx.guild.verification_level) == "high": verification_level = 3
        if str(ctx.guild.verification_level) == "extreme": verification_level = 4

        fields = [("**Owner**",f"{ctx.guild.owner}",True),
                  ("**Created**",f'{ctx.guild.created_at.strftime("%b %d %Y")}',True),
                  (f"**Verification Level [{verification_level}]**",f"{str(ctx.guild.verification_level).title()}",True),

                  (f"**File size limit**",f"{int(ctx.guild.filesize_limit/1000000)} MB",True),
                  (f"**Region**",f"{ctx.guild.region}",True),
                  (f"**Roles**",f"{len(ctx.guild.roles)}",True),
                  
                  ("Channels", f"{Channels[0]} {Channels[1]} {Channels[2]}\n{Channels[3]}\n{Channels[4]}", True),
                  ("Members", f"Total: {Members[0]}\nHumans: {Members[1]}\nBots: {Members[2]}\nBanned: {guild_bans_lenght}", True),
                  ("Emojis",f"Regular: {emojis[0]}\nAnimated: {emojis[1]}\nTotal emojis: {emojis[2]}",True),

                  ("Statuses", f"{online_status_emoji}{statuses[0]} {idle_status_emoji}{statuses[1]} {dnd_status_emoji}{statuses[2]} {offline_status_emoji}{statuses[3]}", False),]

        for name, value, inline in fields:
            em.add_field(name=name, value=value, inline=inline)

        em.set_footer(text=f"ID: {ctx.guild.id}")
        em.timestamp = datetime.utcnow()

        await ctx.reply(embed = em)

    # tserveremojis
    @commands.command(aliases=["se"])
    async def serveremojis(self, ctx, page: int=1):
        try: page = abs(int(page))
        except: page = 1
        if page > 99: page = 99

        output_string = ""
        cycle_int = 0
        for x in ctx.guild.emojis:
            cycle_int = cycle_int + 1
            if cycle_int > ((page*10) - 10) or page == 1:
                if x.animated: output_string += f"**{cycle_int}** - 『{x}』－`<a:{x.name}:{x.id}>`\n"
                else: output_string += f"**{cycle_int}** - 『{x}』－`<:{x.name}:{x.id}>`\n"
            if cycle_int == int(page*10): break

        if output_string != "":
            em = discord.Embed(color=self.client.Blue)
            em.add_field(name=f"Emojis in **{ctx.guild.name}** [{len(ctx.guild.emojis)}]", value=output_string, inline=False)

            em.set_footer(text=f"Page: {page}")
            em.timestamp = datetime.utcnow()
    
            await ctx.send(embed=em)
        else: await ctx.reply(embed = await basic_embed(f"", f"There is nothing here.",self.client.Red,""))
    
    # tserveravatar
    @commands.command(aliases=["sa"])
    async def serveravatar(self, ctx):
        try: guild_icon_url = ctx.guild.icon.url
        except: guild_icon_url = ""
        em = Embed(title=f"",
                   description=f"",
                   colour=self.client.Blue)
        
        em.set_author(name=f"Server Avatar for {ctx.guild}", icon_url = guild_icon_url)

        em.set_image(url=guild_icon_url)
        em.set_footer(text=f"ID: {ctx.guild.id}")
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

################################################################ Zseni ##############################################################
    # tcreator
    @commands.command(aliases=['genius','zseni'])
    async def creator(self, ctx):
        user = await self.client.fetch_user(416508283528937472)
        em = discord.Embed(title = f"{user} is my creator.",
                           description = "Yep, i made the bot.",
                           colour = self.client.Blue,
                           timestamp=datetime.utcnow())
        em.set_thumbnail(url=user.avatar.url)

        em.add_field(name= "Youtube", value = f"[here]({self.client.youtube})", inline=True)
        em.add_field(name= "Discord", value = f"[here](https://discord.gg/SXng95f)", inline=True)
        em.add_field(name= "Twitter", value = f"[here](https://twitter.com/Zseni10)", inline=True)

        await ctx.send(embed = em)
    
############################################################## Functions ############################################################

async def oldest_newest(self, ctx, page, sort_type):
    try: page = abs(int(page))
    except: page = 1
    if page > 99: page = 99

    every_member = []
    for x in ctx.guild.members:
        userinfo = (f"{x} - {x.created_at.strftime('%d/%m/%Y')}", x.created_at)
        every_member.append(userinfo)
    every_member.sort(key=lambda x:x[1])


    if sort_type == "Oldest": every_member_slicled = every_member[((page-1)*10):(page*10)]
    if sort_type == "Newest": every_member_slicled = every_member[(len(every_member)-(((page-1)*10)+1)):((-10*page)-1):-1]

    output_string = ""
    cycle_int = 0
    for x, z in every_member_slicled:
        cycle_int = cycle_int + 1
        output_string += f"**{cycle_int+((page-1)*10)}** - {x}\n"
    
    if output_string != "":
        em = discord.Embed(color=self.client.Blue)
        em.add_field(name=f"{sort_type} accounts in **{ctx.guild.name}**", value=output_string, inline=False)

        em.set_footer(text=f"Page: {page}")
        em.timestamp = datetime.utcnow()
    
        await ctx.send(embed=em)
    else: await ctx.reply(embed = await basic_embed(f"", f"There is nothing here.",self.client.Red,""))


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
    client.add_cog(information(client))
