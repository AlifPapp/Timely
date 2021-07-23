import discord
import json
from datetime import datetime

#####################################################################################################################################
########################################################## C U R R E N C Y ##########################################################
######################################################### F U N C T I O N S #########################################################
#####################################################################################################################################
async def calc_DHMS_left(lifespan_amt):
    if lifespan_amt == 0:
        return 0
    lifespan_amt_days = int(lifespan_amt/86400)
    lifespan_amt_hours = int((lifespan_amt - (lifespan_amt_days * 86400))/3600)
    lifespan_amt_minutes = int((lifespan_amt - (lifespan_amt_days * 86400) - (lifespan_amt_hours * 3600))/60)
    lifespan_amt_seconds = int(lifespan_amt - (lifespan_amt_days * 86400) - (lifespan_amt_hours * 3600) - (lifespan_amt_minutes * 60))

    result = []
    loopcycleint = 0
    loopcycleint2 = 0
    break_at = 2
    appendcalc = [lifespan_amt_days,lifespan_amt_hours,lifespan_amt_minutes,lifespan_amt_seconds]
    for time in appendcalc:
        loopcycleint = loopcycleint + 1
        if time != 0:
            loopcycleint2 = loopcycleint2 + 1
            if loopcycleint == 1: 
                type = "days"
                result.append(f"{time} {type}")
            if loopcycleint == 2: 
                if time == 1: type = "hour"
                else: type = "hours"
                if loopcycleint2 == break_at: 
                    result.append(f" and {time} {type}")
                    break
                result.append(f"{time} {type}")
            if loopcycleint == 3: 
                type = "minutes"
                if loopcycleint2 == break_at: 
                    result.append(f" and {time} {type}")
                    break
                result.append(f"{time} {type}")
            if loopcycleint == 4: 
                type = "seconds"
                if loopcycleint2 == break_at: 
                    result.append(f" and {time} {type}")
                    break
                result.append(f"{time} {type}")
    result = " ".join(result)
    return result

async def open_account(self, ctx, user):
    cluster = self.client.mongodb["Currency"]["Main"]
    userdata = cluster.find_one({"id": user.id})
    if userdata is None:
        DefaultTime = self.client.DefaultTime
        users = {"id": user.id, "savings": 0, "lifespan": DefaultTime,"luck": 0,
                 "commands_used": 0, "stolen": 0,
                 "daily": 0, "weekly": 0, "monthly": 0,
                 "pray": 0}
        cluster.insert_one(users)

        DefaultTimeDays = DefaultTime/86400
        em = discord.Embed(title = f"The clock is ticking {user.name}!",
                           description = f"Start using various commands to gain more time, you only have **{int(DefaultTimeDays)} days** left!",
                           color = self.client.Blue,
                           timestamp=datetime.utcnow())
        try: await user.send(embed = em)
        except: 
            if ctx != None: await ctx.send(embed = em)
    return True

async def user_died(self, ctx, user):
    cluster = self.client.mongodb["Currency"]["Main"]
    await open_account(self, ctx, user)

    DefaultTime = self.client.DefaultTime

    em = discord.Embed(title = f"{user} Died!.",
                   description = "-You met the end of your lifespan. \n-You lost all your items and savings. \n-You get to keep whatever was hidden in your treasure chest.",
                   color = self.client.Red,
                   timestamp=datetime.utcnow())
    try: await user.send(embed = em)
    except: 
        if ctx != None: await ctx.send(embed = em)
    lifespan_amt = DefaultTime
    savings_amt = 0
    cluster.update_one({"id":user.id},{"$set":{"savings":savings_amt}})
    cluster.update_one({"id":user.id},{"$set":{"lifespan":lifespan_amt}})
    return
#####################################################################################################################################
########################################################### G E N E R A L ###########################################################
######################################################### F U N C T I O N S #########################################################
#####################################################################################################################################

async def basic_embed(title, description,color, footer: str=""):
    em = discord.Embed(title = title,
                       description = description,
                       color = color)
    if footer is not None:
        em.set_footer(text=footer)
    em.timestamp = datetime.utcnow()

    return em

#####################################################################################################################################
############################################################ R E D D I T ############################################################
######################################################### F U N C T I O N S #########################################################
#####################################################################################################################################
async def reddit_fill_var(self, guild, subreddit, limit):
    with open("reddit_data.json","r") as f:
        data = json.load(f)
    if f"{subreddit}{guild.id}" not in data:
        data[f"{subreddit}{guild.id}"] = {}

    subreddit = await self.client.reddit.subreddit(subreddit)
    hot = subreddit.hot(limit = limit)

    cycle_int = 0
    async for submission in hot:
        cycle_int = cycle_int + 1
        data[f"{subreddit}{guild.id}"][f"url{cycle_int}"] = submission.url
        data[f"{subreddit}{guild.id}"][f"permalink{cycle_int}"] = submission.permalink
        data[f"{subreddit}{guild.id}"][f"title{cycle_int}"] = submission.title
        data[f"{subreddit}{guild.id}"][f"num_comments{cycle_int}"] = submission.num_comments
        data[f"{subreddit}{guild.id}"][f"score{cycle_int}"] = submission.score
    data[f"{subreddit}{guild.id}"][f"cycle_int"] = cycle_int
    with open("reddit_data.json","w") as f:
        json.dump(data, f)
    return True

async def send_redditpost(self, ctx, subreddit, limit):
    guild = ctx.guild
    msg = None
    with open("reddit_data.json","r") as f: reddit_data = json.load(f)
    if f"{subreddit}{guild.id}" not in reddit_data:
        msg = await ctx.reply(embed = await basic_embed(f"", f"<a:loading:864447463980793896> Loading {limit} posts.",self.client.Blue,""))
        await reddit_fill_var(self, guild, subreddit, limit)
        with open("reddit_data.json","r") as f: reddit_data = json.load(f)
    cycle_int = reddit_data[f"{subreddit}{guild.id}"][f"cycle_int"]
    if cycle_int == 0:
        msg = await ctx.reply(embed = await basic_embed(f"", f"<a:loading:864447463980793896> Loading {limit} posts.",self.client.Blue,""))
        await reddit_fill_var(self, guild, subreddit, limit)
        with open("reddit_data.json","r") as f: reddit_data = json.load(f)
        cycle_int = reddit_data[f"{subreddit}{guild.id}"][f"{subreddit}cycle_int"]

    title =        reddit_data[f"{subreddit}{guild.id}"][f"title{cycle_int}"]
    permalink =    reddit_data[f"{subreddit}{guild.id}"][f"permalink{cycle_int}"]
    url =          reddit_data[f"{subreddit}{guild.id}"][f"url{cycle_int}"]
    score =        reddit_data[f"{subreddit}{guild.id}"][f"score{cycle_int}"]
    num_comments = reddit_data[f"{subreddit}{guild.id}"][f"num_comments{cycle_int}"]

    em = discord.Embed(description = f"[{title}](https://www.reddit.com{permalink})",
                       colour = self.client.Blue,
                       timestamp=datetime.utcnow())
    em.set_image(url = url)
    em.set_footer(text = f"👍{score} 💬{num_comments}")

    if msg == None: await ctx.reply(embed = em)
    else: await msg.edit(embed = em)

    reddit_data[f"{subreddit}{guild.id}"][f"cycle_int"] = cycle_int - 1
    with open("reddit_data.json","w") as f:
        json.dump(reddit_data, f)


        