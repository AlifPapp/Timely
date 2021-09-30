import discord
from discord.ext.commands import Cog
from datetime import datetime
from discord_slash import cog_ext, SlashContext

client = discord.Client
client.guild_ids = [835851709884530738]

class slash_cmds(Cog):
    def __init__(self, client):
        self.client = client

    @Cog.listener()
    async def on_ready(self):
        print("slash_cmds.py Loaded!")
        #client.guild_ids = [835851709884530738]
        #for guild in client.guilds: client.guild_ids.append(int(guild.id))

    async def cog_check(self, ctx):
        try: 
            if ctx.guild is not None and not ctx.author.bot: return True
        except: pass
    
    
    
    @cog_ext.cog_slash(name="help", description="Help get you started", guild_ids=client.guild_ids)
    async def help(self, ctx: SlashContext):
        p = self.client.serverprefix
        em = discord.Embed(title = "List of commands",
                           description = f"**Prefix:** `{p}` and {self.client.user.mention}\nIf you have any questions/queries feel free to join the [support server](https://discord.gg/E8DnTgMvMW)",
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())
        em.add_field(name="<:coin:862881131799248937> Currency",value=f"`{p}help currency`",inline=True)
        em.add_field(name="<:count:862882885916033054> Counting",value = f"`{p}help counting`",inline=True)
        em.add_field(name="<:reddit_icon:869174075250061343> reddit",value = f"`{p}help reddit`",inline=True)
        em.add_field(name="<:info:862881844265746442> Informational",value = f"`{p}help informational`",inline=True)
        em.add_field(name="<:static_cog:862507223062151168> Settings",value = f"`{p}help settings`",inline=True)

        await ctx.send(embed = em)

#####################################################################################################################################
def setup(client):
    client.add_cog(slash_cmds(client))

#'cogs.slash_cmds',

#from discord_slash import SlashCommand
#slash = SlashCommand(client, sync_commands=True)

#Remove guild.id to array of guild ids
#    client.guild_ids.remove(guild.id)

#Add guild.id to array of guild ids
#    client.guild_ids.append(guild.id)
