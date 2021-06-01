import discord
from discord import user, client
from discord.ext import commands

from datetime import datetime

import ssl
from pymongo import MongoClient
from datetime import datetime



#####################################################################################################################################
######################################################### GET SERVER PREFIX #########################################################
#####################################################################################################################################
async def get_prefix(client,ctx):
    if ctx.guild is None:
        client.serverprefix = "t"
        return commands.when_mentioned_or("t","T")(client,ctx)

    guild = client.serverprefixcluster.find_one({"guild_id": str(ctx.guild.id)})
    
    if guild is None:
        guilds = {"guild_id": str(ctx.guild.id), "prefix": "t"}
        client.serverprefixcluster.insert_one(guilds)
        client.serverprefix = "t"
        return commands.when_mentioned_or("t","T")(client,ctx)

    client.serverprefix = guild["prefix"]
    if client.serverprefix == "t":
        return commands.when_mentioned_or("t","T")(client,ctx)
    return commands.when_mentioned_or(client.serverprefix)(client,ctx)

#####################################################################################################################################
############################################################ C L I E N T ############################################################
#####################################################################################################################################
intents = discord.Intents.all()
client = commands.Bot(command_prefix = get_prefix,
                      case_insensitive=True,
                      intents = intents)
client.remove_command('help')


#####################################################################################################################################
############################################################# VARIABLES #############################################################
#####################################################################################################################################
client.developerid = 416508283528937472, 615293601408090113
client.cooldown = []
client.DefaultTime = 604800

client.Yellow = int("FFB744" , 16)
client.Black = int("000000" , 16)
client.Green = int("3BA55C" , 16)
client.Red = int("D72D42" , 16)
client.Blue = int("7289DA" , 16)

MongoClientLink = open("MongoClient.txt","r").readline()
cluster = MongoClient(MongoClientLink.strip(), ssl_cert_reqs=ssl.CERT_NONE)
client.currencydata = cluster["Currency"]["Main"]
client.serverprefixcluster = cluster["Settings"]["ServerPrefix"]

#####################################################################################################################################
############################################################## C O G S ##############################################################
#####################################################################################################################################
initial_extensions = ['cogs.currency',
                      'cogs.other',
                      'cogs.help',
                      'cogs.moderation',
                      'cogs.music',
                      #'cogs.error',
                      #'cogs.beta'
                      'cogs.developer']
if __name__ == '__main__':
    for extension in initial_extensions:
        client.load_extension(extension)


#####################################################################################################################################
############################################################### EVENTS ##############################################################
#####################################################################################################################################
@client.event
async def on_ready():
    print('Logged in as')
    print('Name:', client.user.name)
    print('ID:', client.user.id)
    print('------')
    servers = len(client.guilds)
    await client.change_presence(activity=discord.Game(f'thelp | {servers} servers'))
    print('Main.py Loaded!')

    channel = client.get_channel(845586893789986857)
    em = discord.Embed(title = "TimelyBot has awoken!",
                           description = "But for how long?",
                           color = client.Blue,
                           timestamp=datetime.utcnow())
    await channel.send(embed = em)

@client.event
async def on_connect():
    print("Bot has connected")

@client.event
async def on_disconnect():
    print("Bot has disconnected")

@client.event
async def on_guild_join(guild):
    guild = client.serverprefixcluster.find_one({"guild_id": str(guild.id)})
    if guild is None:
        guilds = {"guild_id": str(user.id), "prefix": "t"}
        client.serverprefixcluster.insert_one(guilds)


#####################################################################################################################################
########################################################### PREFIX COMMANDS #########################################################
#####################################################################################################################################
@client.command()
async def prefix(ctx):
    guild = client.serverprefixcluster.find_one({"guild_id": str(ctx.guild.id)})
    serverprefix = guild["prefix"]

    em = discord.Embed(title = "Prefixes",
                           description = f"**1:**{client.user.mention}\n**2:** `{serverprefix}`",
                           colour = client.Blue,
                           timestamp=datetime.utcnow())
    em.add_field(name= "Change the prefix?", value = "Try: `changeprefix <newprefix>`", inline=True)
    await ctx.send(embed = em)

@client.command()
async def changeprefix(ctx, newprefix: str="None"):
    if ctx.author.guild_permissions.administrator:
        if newprefix == "None":
            em = discord.Embed(description = "What do you expect me to change it to??",
                               color = client.Red,
                               timestamp=datetime.utcnow())
            await ctx.reply(embed = em)
            return

        client.serverprefixcluster.update_one({"guild_id":str(ctx.guild.id)},{"$set":{"prefix":newprefix}})
        em = discord.Embed(description = f"Prefix successfully changed to `{newprefix}`.",
                           colour = client.Blue,
                           timestamp=datetime.utcnow())
        await ctx.send(embed = em)
    else:
        em = discord.Embed(description = f"{ctx.author.mention} you don't have the permission `administrator` to do that!",
                               color = client.Red,
                               timestamp=datetime.utcnow())
        await ctx.reply(embed = em)

#####################################################################################################################################
token = open("token.txt","r").readline()
client.run(token.strip())
