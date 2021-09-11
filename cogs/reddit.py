import discord
import json
import asyncio

from discord.ext import commands
from datetime import datetime

from .functions import basic_embed

class reddit(commands.Cog):
    def __init__(self, client):
        self.client = client
        

    @commands.Cog.listener()
    async def on_ready(self):
        print("reddit.py Loaded!")
    
    async def cog_check(self, ctx):
        if ctx.guild is not None: return True
        if not ctx.author.bot: return True

    @commands.command() 
    async def redditleaderboard(self, ctx, time: str="all", page: str="1"):
        try: 
            page = int(time)
            time = "alltime"
        except:
            if time in ("all","alltime","eternity"): time = "alltime"
            if time in ("month","monthly","thismonth"): time = "monthlytime"
            if time in ("week","weekly","thisweek"): time = "weeklytime"
            if time in ("today","now"): time = "today"
            
            if time not in ("alltime","monthlytime","weeklytime","today"): time = "alltime"
        
        try: page = abs(int(page))
        except: page = 1
        if page > 99: page = 99

        cluster = self.client.mongodb["Reddit"]["Leaderboard"]
        list_of_subreddits = cluster.find().sort(time, -1)

        string = ""
        cycle_int = 0
        for x in list_of_subreddits:
            if x[time] != 0:
                cycle_int = cycle_int + 1
                string += f"**{cycle_int}** - [r/{x['subreddit']}](https://www.reddit.com/r/{x['subreddit']})\n"
                if cycle_int == int(page*10): break # or len(list_of_subreddits)
    
        if string == "":
            await ctx.reply(embed = await basic_embed(f"", f"There is nothing here.",self.client.Red,""))
            return
        
        em = discord.Embed(color=self.client.Blue)
        if time == "alltime":     em.add_field(name=f"Top subreddits of all time", value=string, inline=False)
        if time == "monthlytime": em.add_field(name=f"Top subreddits of this month", value=string, inline=False)
        if time == "weeklytime":  em.add_field(name=f"Top subreddits of this week", value=string, inline=False)
        if time == "today":       em.add_field(name=f"Top subreddits today", value=string, inline=False)

        em.set_footer(text=f"Page: {page}")
        em.timestamp = datetime.utcnow()
        
        await ctx.send(embed=em)

    @commands.command()
    async def redditsearch(self, ctx, subreddit):
        emoji = "<:refresh:874122192143679528>"
        limit = 100
        
        #input arg error
        if subreddit[0:2] != "r/" or subreddit == None:
            await ctx.reply(embed = await basic_embed(f"", f"<:danger:848526668024250408> incorrect syntax.",self.client.Red,f"{self.client.serverprefix}redditsearch r/subreddit"))
            return
        subreddit = subreddit[2::]
        await reddit_send(self, ctx, subreddit, emoji, limit)

#####################################################################################################################################
async def reddit_fill_var(self, subreddit, limit):
    with open("reddit_data.json","r") as f:
        data = json.load(f)
    if f"{subreddit}" not in data:
        data[f"{subreddit}"] = {}

    subreddit = await self.client.reddit.subreddit(subreddit)
    
    new = subreddit.new(limit = limit)

    cycle_int = 0
    try: 
        async for submission in new:
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
            await msg.edit(embed = await basic_embed(f"", f"<:danger:848526668024250408> subreddit: [r/{subreddit}](https://www.reddit.com/r/{subreddit}) could not be found.",self.client.Red,""))
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
    em.set_footer(text = f"👍{submission.score} 💬{submission.num_comments} r/{subreddit.lower()}")

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
        reddit = cluster.find_one({"subreddit": subreddit.lower()})
        if reddit is None:
            reddit_insert = {"subreddit": subreddit.lower(), 
                             "alltime": 1,
                             "monthlytime": 1,
                             "weeklytime": 1,
                             "reset_countdown": 86400}
            day = 1
            while day != 31:
                reddit_insert[f"day{day}"] = 0
                day = day + 1
                reddit_insert[f"day{1}"] = 1
            cluster.insert_one(reddit_insert)
        else:
            cluster.update_one({"subreddit": subreddit.lower()},{"$set":{"alltime": (reddit["alltime"]+1) }})
            cluster.update_one({"subreddit": subreddit.lower()},{"$set":{f"day1": (reddit[f"day1"]+1) }})

    #Check for user reaction
    def check(reaction, user):
        return user.bot == False and str(reaction.emoji) == emoji and reaction.message == msg

    try: 
        reaction, user = await self.client.wait_for('reaction_add', timeout=120.0, check=check)
    except asyncio.TimeoutError: 
        await msg.remove_reaction(emoji, self.client.user)
        return

    if str(reaction.emoji) == emoji:
        await msg.remove_reaction(emoji, self.client.user)
        await reddit_send(self, msg, subreddit, emoji, limit)
        return

#####################################################################################################################################
def setup(client):
    client.add_cog(reddit(client))
