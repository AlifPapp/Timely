import discord
from discord import client
from discord.ext import commands

import ssl
import os
import asyncpraw
from pymongo import MongoClient
from datetime import datetime


defaultprefix = "t"
#####################################################################################################################################
######################################################### GET SERVER PREFIX #########################################################
#####################################################################################################################################
async def get_prefix(client, ctx):
    cluster = client.mongodb["Settings"]["ServerPrefix"]
    if ctx.guild is None:
        client.serverprefix = defaultprefix
        upperserverprefix = client.serverprefix.upper()
        return commands.when_mentioned_or(upperserverprefix, client.serverprefix)(client, ctx)

    guild = cluster.find_one({"guild_id": str(ctx.guild.id)})
    
    if guild is None:
        guilds = {"guild_id": str(ctx.guild.id), "prefix": defaultprefix}
        cluster.insert_one(guilds)
        client.serverprefix = defaultprefix
        upperserverprefix = client.serverprefix.upper()
        return commands.when_mentioned_or(upperserverprefix, client.serverprefix)(client, ctx)

    client.serverprefix = guild["prefix"]
    upperserverprefix = client.serverprefix.upper()
    return commands.when_mentioned_or(upperserverprefix, client.serverprefix)(client, ctx)


#####################################################################################################################################
############################################################ C L I E N T ############################################################
#####################################################################################################################################
intents = discord.Intents.all()
client = commands.Bot(command_prefix = get_prefix,
                      case_insensitive=True,
                      intents = intents,
                      status=discord.Status.idle)
client.remove_command('help')

#####################################################################################################################################
############################################################# VARIABLES #############################################################
#####################################################################################################################################
client.developerid = 416508283528937472, 615293601408090113, 566931386305609728
client.cooldown = []
client.DefaultTime = 604800

client.Yellow = int("FFB744" , 16)
client.Black = int("000000" , 16)
client.Green = int("2EC550" , 16)
client.Red = int("D72D42" , 16)
client.Blue = int("7289DA" , 16)

client.reddit = asyncpraw.Reddit(client_id='I3OPzaRVRoxfDcHwiK5afg',
                client_secret='lDSn3SnYCeXtImvRyXHshGtiVHv38A',
                user_agent='phyton_praw')

#MongoClientLink = open("MongoClient.txt","r").readline()
#client.mongodb = MongoClient(MongoClientLink.strip(), ssl_cert_reqs=ssl.CERT_NONE)
client.mongodb = MongoClient(str(os.environ.get('MONGO_LINK')), ssl_cert_reqs=ssl.CERT_NONE)

#####################################################################################################################################
############################################################## C O G S ##############################################################
#####################################################################################################################################
initial_extensions = ['cogs.currency',
                      'cogs.music',
                      'cogs.moderation',
                      'cogs.information',
                      'cogs.help',
                      'cogs.counting',
                      'cogs.nsfw',
                      'cogs.backgroundtasks',
                      'cogs.error',
                      'cogs.beta',
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
    await client.change_presence(activity=discord.Streaming(name=f'thelp to {len(client.guilds)} servers', url="https://www.twitch.tv/zseni_51"))
    print('Main.py Loaded!')

@client.event
async def on_connect():
    print("Bot has connected")

@client.event
async def on_disconnect():
    print("Bot has disconnected")

@client.event
async def on_guild_join(guild):
    cluster = client.mongodb["Settings"]["ServerPrefix"]
    #Setup default prefix
    guilds = cluster.find_one({"guild_id": str(guild.id)})
    if guilds is None:
        guilds = {"guild_id": str(guild.id), "prefix": defaultprefix}
        cluster.insert_one(guilds)
    
    if client.user.id != 836198930873057290:
        return
    channel = client.get_channel(850241543495352351)
    em = discord.Embed(title = "Joined Server",
                       description = f"**Name:** {guild}\n**ID:** {guild.id}\n**MemberCount:** {guild.member_count}\n**New GuildCount:** {len(client.guilds)}",
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
    cluster = client.mongodb["Settings"]["ServerPrefix"]
    guild = cluster.find_one({"guild_id": str(ctx.guild.id)})
    serverprefix = guild["prefix"]

    em = discord.Embed(title = "Prefixes",
                           description = f"**1:**{client.user.mention}\n**2:** `{serverprefix}`",
                           colour = client.Blue,
                           timestamp=datetime.utcnow())
    em.add_field(name= "Change the prefix?", value = f"Try: `{serverprefix}changeprefix <newprefix>`", inline=True)
    await ctx.send(embed = em)

@client.command()
async def changeprefix(ctx, newprefix: str="None"):
    cluster = client.mongodb["Settings"]["ServerPrefix"]
    if ctx.author.guild_permissions.administrator:
        if newprefix == "None":
            em = discord.Embed(description = f"<:danger:848526668024250408> No newprefix was specified",
                           color = client.Red,
                           timestamp=datetime.utcnow())
            await ctx.reply(embed = em)
            return

        cluster.update_one({"guild_id":str(ctx.guild.id)},{"$set":{"prefix":newprefix}})
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
