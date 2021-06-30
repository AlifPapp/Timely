import discord 
from discord.ext import commands

from datetime import datetime
from typing import Optional

from discord import Embed, Member

import psutil

class information(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("other.py Loaded!")

    async def cog_check(self, ctx):
        if ctx.guild is not None: return True
        if not ctx.author.bot: return True

############################################################## Bot Info #############################################################
    # tinvite
    @commands.command()
    async def invite(self, ctx):
        em = discord.Embed(title = "",
                           description = "",
                           colour = self.client.Blue,
                           timestamp=datetime.utcnow())
        admin_invitelink = "[admin_perms](https://discord.com/api/oauth2/authorize?client_id=836198930873057290&permissions=8&scope=bot)"
        choice_invitelink = "[choose_perms](https://discord.com/api/oauth2/authorize?client_id=836198930873057290&permissions=4294967287&scope=bot)"
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

        fields = [(":file_folder:Info",f"Owner: {Vars[0]}\nCreated: {Vars[1]}\nGuilds: {Vars[2]}\nUsers: {users_sum}",False),
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

        #Find what platform target is using
        status_string = ""
        if target.desktop_status == discord.Status.online: status_string += "<:desktop_online:853461125697241108>"
        if target.desktop_status == discord.Status.idle: status_string += "<:desktop_idle:853461158068879370>"
        if target.desktop_status == discord.Status.dnd: status_string += "<:desktop_dnd:853461186132312105>"

        if target.mobile_status == discord.Status.online: status_string += "<:mobile_online:853458040858214400>"
        if target.mobile_status == discord.Status.idle: status_string += "<:mobile_idle:853460184071143424>"
        if target.mobile_status == discord.Status.dnd: status_string += "<:mobile_dnd:853460245823881256>"

        if target.web_status == discord.Status.online: status_string += "<:browser_online:853462294906011698>"
        if target.web_status == discord.Status.idle: status_string += "<:browser_idle:853462332507422741>"
        if target.web_status == discord.Status.dnd: status_string += "<:browser_dnd:853462360476090399>"

        if status_string == "": status_string = "NA"

        em = Embed(title=f"User Info - {target}",
                   description=f"{target.mention} [{status_string}]",
                   colour=self.client.Blue)
        em.set_thumbnail(url=target.avatar_url)

        for name, value, inline in fields:
        	em.add_field(name=name, value=value, inline=inline)

        em.set_footer(text=f"ID: {ctx.author.id}")
        em.timestamp = datetime.utcnow()

        await ctx.reply(embed = em)

    # tavatar
    @commands.command(aliases=['av'])
    async def avatar(self, ctx, target: Optional[Member]):
        user = target or ctx.author

        em = Embed(title=f"",
                   description=f"",
                   colour=self.client.Blue)
        
        em.set_author(name=f"{user}'s Avatar", icon_url = user.avatar_url)

        em.set_image(url=user.avatar_url)
        em.set_footer(text=f"ID: {user.id}")
        em.timestamp = datetime.utcnow()

        await ctx.reply(embed = em)

############################################################# Server Info ###########################################################
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
                   len(list(filter(lambda m: m.bot, ctx.guild.members)))]

        try:
            guild_bans_lenght = len(await ctx.guild.bans())
        except discord.Forbidden:
            guild_bans_lenght = f"MissingPerms"

        Channels = [len(ctx.guild.text_channels),
                    len(ctx.guild.voice_channels),
                    len(ctx.guild.categories)]

        Info = [ctx.guild.owner,
                ctx.guild.created_at.strftime("%d/%m/%Y"),
                ctx.guild.region,
                len(ctx.guild.roles)]

        online_status_emoji = "<:online_status:851753067611553803>"
        idle_status_emoji = "<:idle_status:851753110132228106>"
        dnd_status_emoji = "<:dnd_status:851753181859151872>"
        offline_status_emoji = "<:offline_status:851753226407641098>"

        fields = [("Info",f"Owner: {Info[0]}\nCreated: {Info[1]}\nVoice region: {Info[2]}\nRoles: {Info[3]}",True),
                  ("Channels", f"<:text_channel:846217104381575238> {Channels[0]}\n<:voice_channel:846217088535494707> {Channels[1]}\n<:category:846219026123849749> {Channels[2]}", True),
                  ("Members", f"Total: {Members[0]}\nHumans: {Members[1]}\nBots: {Members[2]}\nBanned: {guild_bans_lenght}", True),
                  ("Statuses", f"{online_status_emoji}{statuses[0]} {idle_status_emoji}{statuses[1]} {dnd_status_emoji}{statuses[2]} {offline_status_emoji}{statuses[3]}", True)]

        for name, value, inline in fields:
            em.add_field(name=name, value=value, inline=inline)

        em.set_footer(text=f"ID: {ctx.guild.id}")
        em.timestamp = datetime.utcnow()

        await ctx.reply(embed = em)

    # tserveremojis
    @commands.command(aliases=["se"])
    async def serveremojis(self, ctx, page: int=1):
        page = abs(int(page))
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
        else: await ctx.send("Nothing here.")
    
    # tserveravatar
    @commands.command(aliases=["sa"])
    async def serveravatar(self, ctx):

        em = Embed(title=f"",
                   description=f"",
                   colour=self.client.Blue)
        
        em.set_author(name=f"Server Avatar for **{ctx.guild}**", icon_url = ctx.guild.icon_url)

        em.set_image(url=ctx.guild.icon_url)
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



#####################################################################################################################################
######################################################## D E V E L O P E R S ########################################################
#####################################################################################################################################
    # tdevelopers
    @commands.command()
    async def developers(self, ctx):
        p = self.client.serverprefix
        em = discord.Embed(title = "List of Developers",
                           description = "> Zseni\n> MinuteLad\n> nyquil",
                           colour = self.client.Blue,
                           timestamp=datetime.utcnow())
    
        em.add_field(name="Usage:",value = f"`{p}<developer>`‏‏‎")

        await ctx.send(embed = em)

    # tcreator
    @commands.command(aliases=['genius','zseni'])
    async def creator(self, ctx):
        em = discord.Embed(title = "Zseni#5848 is my creator.",
                           description = "Yep, i made the bot.",
                           colour = self.client.Blue,
                           timestamp=datetime.utcnow())
        em.set_thumbnail(url="https://imgur.com/wSnPFbH.gif")

        em.add_field(name= "Youtube", value = "[here](http://bit.ly/Zseni-Youtube )", inline=True)
        em.add_field(name= "Discord", value = "[here](https://discord.gg/SXng95f)", inline=True)
        em.add_field(name= "Twitter", value = "[here](https://twitter.com/Zseni10)", inline=True)

        await ctx.send(embed = em)
    
    # tnyquil
    @commands.command(aliases=['ghost'])
    async def nyquil(self, ctx):
        timely_supportserver = self.client.get_guild(835851709884530738)
        nyquil = timely_supportserver.get_member(615293601408090113)

        em = discord.Embed(title = f"{nyquil} is the owner of **Dank Vibes**.",
                           description = f"He likes to lurk in {self.client.user.mention}'s support server",
                           colour = self.client.Blue,
                           timestamp=datetime.utcnow())
        em.set_thumbnail(url=nyquil.avatar_url)

        em.add_field(name= "Dank Vibes", value = "[here](https://discord.gg/dankmemer)", inline=True)

        await ctx.send(embed = em)
    
    # tminutelad
    @commands.command()
    async def minutelad(self, ctx):
        timely_supportserver = self.client.get_guild(835851709884530738)
        minutelad = timely_supportserver.get_member(566931386305609728)

        em = discord.Embed(title = f"{minutelad} is the one who started it all.",
                           description = f'He is the one who wanted to make a discord bot currency system based of the movie "In Time"',
                           colour = self.client.Blue,
                           timestamp=datetime.utcnow())
        em.set_thumbnail(url=minutelad.avatar_url)

        await ctx.send(embed = em)


async def oldest_newest(self, ctx, page, sort_type):
    page = abs(int(page))
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
    else: await ctx.send("Nothing here.")


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