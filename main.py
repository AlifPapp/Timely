import discord
import ssl
import os
import asyncpraw
import json

from pymongo import MongoClient
from datetime import datetime
from discord.ext import commands

defaultprefix = "t"
botishosted = True

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

class Bot(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(command_prefix = get_prefix,
                         case_insensitive=True,
                         intents = discord.Intents.all(),
                         status = discord.Status.idle,
                        activity=discord.Activity(type=discord.ActivityType.listening , name=f"thelp"))
        self.remove_command('help')
        
        with open("./json/emoji.json","r") as f: 
            self.Emojis = json.load(f)
        
        if botishosted == True:
            self.Secrets = json.loads(os.environ.get('Secrets'))
        else: 
            with open("./json/Secrets.json","r") as f: 
                self.Secrets = json.load(f)

        self.youtube = "https://www.youtube.com/channel/UCsIaU94p647veKr7sy12wmA"
        self.developerid = 416508283528937472, 615293601408090113, 566931386305609728
        self.cooldown = []
        self.DefaultTime = 604800

        self.Yellow = int("FFB744" , 16)
        self.Black = int("000000" , 16)
        self.Green = int("2EC550" , 16)
        self.Red = int("D72D42" , 16)
        self.Blue = int("7289DA" , 16)

        self.reddit = asyncpraw.Reddit(client_id=self.Secrets["Reddit_client_id"],
                                       client_secret=self.Secrets["Reddit_client_secret"],
                                       user_agent='phyton_praw')
        self.mongodb = MongoClient(self.Secrets["MongoClientLink"], ssl_cert_reqs=ssl.CERT_NONE)

        initial_extensions = ['cogs.help',
                              'cogs.currency',
                              'cogs.reddit',
                              'cogs.information',
                              'cogs.other',
                              'cogs.backgroundtasks',
                              'cogs.error',
                              'cogs.creator_cmds']
        for extension in initial_extensions:
            self.load_extension(extension)
        
    async def on_ready(self):
        print('Logged in as')
        print('Name:', self.user.name)
        print('ID:', self.user.id)
        print('------')
        print('Main.py Loaded!')

    async def on_connect(self):
        print("Bot has connected")

    async def on_disconnect(self):
        print("Bot has disconnected")
client = Bot()

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
client.run(client.Secrets["Token"])
