import discord
import json
import asyncio

from discord.ext import commands
from datetime import datetime

from .functions import basic_embed

class nsfw(commands.Cog):
    def __init__(self, client):
        self.client = client
        

    @commands.Cog.listener()
    async def on_ready(self):
        print("reddit.py Loaded!")
    
    async def cog_check(self, ctx):
        if ctx.guild is not None: return True
        if not ctx.author.bot: return True


    @commands.command()
    async def redditsearch(self, ctx, subreddit):
        emoji = "<:refresh:874122192143679528>"
        limit = 10
        
        #input arg error
        if subreddit[0:2] != "r/" or subreddit == None:
            await ctx.reply(embed = await basic_embed(f"", f"<:danger:848526668024250408> incorrect syntax.",self.client.Red,f"{self.client.serverprefix}redditsearch r/subreddit"))
            return
        subreddit = subreddit[2::]
        await reddit_send(self, ctx, subreddit, emoji, limit)

    @commands.command()
    async def redditleaderboard(self, ctx):#, subreddit):
        await ctx.send("comming very soon")
        return

#####################################################################################################################################
async def reddit_fill_var(self, subreddit, limit):
    with open("reddit_data.json","r") as f:
        data = json.load(f)
    if f"{subreddit}" not in data:
        data[f"{subreddit}"] = {}

    subreddit = await self.client.reddit.subreddit(subreddit)
    
    hot = subreddit.hot(limit = limit)

    cycle_int = 0
    try: 
        async for submission in hot:
            cycle_int = cycle_int + 1
            data[f"{subreddit}"][f"s{cycle_int}"] = submission.id
    except: return False
    
    with open("reddit_data.json","w") as f:
        json.dump(data, f)
    return True

async def reddit_send(self, ctx, subreddit, emoji, limit):
    guild = ctx.guild
    msg = None
    could_not_be_found = False

    if ctx.author.id == self.client.user.id: 
        msg = await ctx.reply(embed = await basic_embed(f"", f"<a:loading:864447463980793896> Loading submission.",self.client.Blue,""))

    #stores submission if not already stored
    with open("reddit_data.json","r") as f: reddit_data = json.load(f)
    if f"{subreddit}" not in reddit_data:
        msg = await ctx.reply(embed = await basic_embed(f"", f"<a:loading:864447463980793896> Loading {limit} submissions.",self.client.Blue,""))
        if await reddit_fill_var(self, subreddit, limit) == False: 
            await ctx.edit(embed = await basic_embed(f"", f"<:danger:848526668024250408> subreddit: *r/{subreddit}* could not be found.",self.client.Red,""))
            could_not_be_found = True
        with open("reddit_data.json","r") as f: reddit_data = json.load(f)
    
    #adds submission cycle_int for individual guild's if its missing.
    if f"{subreddit}{guild.id}" not in reddit_data:
        reddit_data[f"{subreddit}{guild.id}"] = {}
        reddit_data[f"{subreddit}{guild.id}"][f"cycle_int"] = 1
    
    #retrive submission from local storage
    cycle_int = reddit_data[f"{subreddit}{guild.id}"][f"cycle_int"]
    submission = await self.client.reddit.submission(reddit_data[f"{subreddit}"][f"s{cycle_int}"])
    
    #check if submission is marked over_18
    if submission.over_18:
        if ctx.channel.is_nsfw() == False:
            em = await basic_embed(f"", f"<:danger:848526668024250408> Prohibited not a nsfw channel.",self.client.Red,"")
            if msg == None: await ctx.reply(embed = em)
            else: await msg.edit(embed = em)
            return

    #setup embed
    em = discord.Embed(description = f"[{submission.title}](https://www.reddit.com{submission.permalink})",
                       colour = self.client.Blue,
                       timestamp=datetime.utcnow())
    em.set_image(url = submission.url)
    em.set_footer(text = f"👍{submission.score} 💬{submission.num_comments}")

    #send embed and add reaction
    if msg == None: 
        msg = await ctx.reply(embed = em)
        await msg.add_reaction(emoji)
    else: 
        await msg.edit(embed = em)
        await msg.add_reaction(emoji)

    #Update cycle_int to json
    cycle_int = cycle_int + 1
    if cycle_int == (limit + 1): cycle_int = 1
    reddit_data[f"{subreddit}{guild.id}"][f"cycle_int"] = cycle_int

    with open("reddit_data.json","w") as f:
        json.dump(reddit_data, f)

    #Mongo DB - Leaderboard
    if could_not_be_found == False:
        cluster = self.client.mongodb["Reddit"]["Leaderboard"]
        reddit = cluster.find_one({"subrredit": subreddit})
        if reddit is None:
            reddit_insert = {"subrredit": subreddit, 
                             "alltime": 1,
                             "reset_countdown": 86400}
            day = 1
            while day != 31:
                reddit_insert[f"day{day}"] = 0
                day = day + 1
                reddit_insert[f"day{1}"] = 1
            cluster.insert_one(reddit_insert)
        else:
            cluster.update_one({"subrredit": subreddit},{"$set":{"alltime": (reddit["alltime"]+1) }})
            cluster.update_one({"subrredit": subreddit},{"$set":{f"day1": (reddit[f"day1"]+1) }})

    #Check for user reaction
    def check(reaction, user):
        return user.bot == False and str(reaction.emoji) == emoji and reaction.message == msg

    try: 
        reaction, user = await self.client.wait_for('reaction_add', timeout=30.0, check=check)
    except asyncio.TimeoutError: 
        await msg.remove_reaction(emoji, self.client.user)
        return

    if str(reaction.emoji) == emoji:
        await msg.remove_reaction(emoji, self.client.user)
        await reddit_send(self, msg, subreddit, emoji, limit)
        return

#####################################################################################################################################
def setup(client):
    client.add_cog(nsfw(client))
