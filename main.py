import discord
from discord import user, client
from discord.ext import commands

from datetime import datetime

import ssl
import os
from pymongo import MongoClient
from datetime import datetime


defaultprefix = "t"
#####################################################################################################################################
######################################################### GET SERVER PREFIX #########################################################
#####################################################################################################################################
async def get_prefix(client,ctx):
    if ctx.guild is None:
        client.serverprefix = defaultprefix
        upperserverprefix = client.serverprefix.upper()
        return commands.when_mentioned_or(upperserverprefix, client.serverprefix)(client,ctx)

    guild = client.serverprefixcluster.find_one({"guild_id": str(ctx.guild.id)})
    
    if guild is None:
        guilds = {"guild_id": str(ctx.guild.id), "prefix": defaultprefix}
        client.serverprefixcluster.insert_one(guilds)
        client.serverprefix = defaultprefix
        upperserverprefix = client.serverprefix.upper()
        return commands.when_mentioned_or(upperserverprefix, client.serverprefix)(client,ctx)

    client.serverprefix = guild["prefix"]
    if client.serverprefix == defaultprefix:
        upperserverprefix = client.serverprefix.upper()
        return commands.when_mentioned_or(upperserverprefix, client.serverprefix)(client,ctx)
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

#MongoClientLink = open("MongoClient.txt","r").readline()
#cluster = MongoClient(MongoClientLink.strip(), ssl_cert_reqs=ssl.CERT_NONE)
cluster = MongoClient(str(os.environ.get('MONGO_LINK')), ssl_cert_reqs=ssl.CERT_NONE)
client.currencydata = cluster["Currency"]["Main"]
client.serverprefixcluster = cluster["Settings"]["ServerPrefix"]

#####################################################################################################################################
############################################################## C O G S ##############################################################
#####################################################################################################################################
initial_extensions = ['cogs.currency',
                      'cogs.utility',
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
    await client.change_presence(activity=discord.Game(f'thelp | {len(client.guilds)} servers'))
    print('Main.py Loaded!')

    #Send to channel that it`s online
    if client.user.id != 836198930873057290:
        return
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
    #Setup default prefix
    guilds = client.serverprefixcluster.find_one({"guild_id": str(guild.id)})
    if guilds is None:
        guilds = {"guild_id": str(guild.id), "prefix": defaultprefix}
        client.serverprefixcluster.insert_one(guilds)
    
    if client.user.id != 836198930873057290:
        return
    channel = client.get_channel(850241543495352351)
    em = discord.Embed(title = "Joined Server",
                       description = f"**Name:** {guild}\n**ID:** {guild.id}\n**MemberCount:** {guild.member_count}\n**New Bot's GuildCount:** {len(client.guilds)}",
                       color = client.Blue,
                       timestamp=datetime.utcnow())
    await channel.send(embed = em)

@client.event
async def on_guild_remove(guild):
    if client.user.id != 836198930873057290:
        return
    channel = client.get_channel(850241543495352351)
    em = discord.Embed(title = "Left Server",
                       description = f"**Name:** {guild}\n**ID:** {guild.id}\n**MemberCount:** {guild.member_count}\n**New Bot's GuildCount:** {len(client.guilds)}",
                       color = client.Red,
                       timestamp=datetime.utcnow())
    await channel.send(embed = em)


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
    em.add_field(name= "Change the prefix?", value = f"Try: `{serverprefix}changeprefix <newprefix>`", inline=True)
    await ctx.send(embed = em)

@client.command()
async def changeprefix(ctx, newprefix: str="None"):
    if ctx.author.guild_permissions.administrator:
        if newprefix == "None":
            em = discord.Embed(description = f"<:danger:848526668024250408> No newprefix was specified",
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
        em = discord.Embed(description = f"<:danger:848526668024250408> You are missing the permission `administrator`.",
                           color = client.Red,
                           timestamp=datetime.utcnow())
        await ctx.reply(embed = em)

#####################################################################################################################################
#token = open("token.txt","r").readline()
#client.run(token.strip())
client.run(str(os.environ.get('BOT_TOKEN')))
