import discord
from datetime import datetime

#####################################################################################################################################
########################################################## C U R R E N C Y ##########################################################
######################################################### F U N C T I O N S #########################################################
#####################################################################################################################################
async def calc_DHMS_left(lifespan_amt):
    lifespan_amt_days = int(lifespan_amt/86400)
    lifespan_amt_hours = int((lifespan_amt - (lifespan_amt_days * 86400))/3600)
    lifespan_amt_minutes = int((lifespan_amt - (lifespan_amt_days * 86400) - (lifespan_amt_hours * 3600))/60)
    lifespan_amt_seconds = int(lifespan_amt - (lifespan_amt_days * 86400) - (lifespan_amt_hours * 3600) - (lifespan_amt_minutes * 60))

    result = []
    loopcycleint = 0
    appendcalc = [lifespan_amt_days,lifespan_amt_hours,lifespan_amt_minutes,lifespan_amt_seconds]
    for time in appendcalc:
        loopcycleint = loopcycleint + 1
        if time != 0:
            if loopcycleint == 1: type = "days"
            if loopcycleint == 2: type = "hours"
            if loopcycleint == 3: type = "minutes"
            if loopcycleint == 4: type = result.append(f" and {time} seconds")
            else:
                result.append(f"{time} {type}")
    result = ", ".join(result)
    return result

async def open_account(self, ctx, user):
    cluster = self.client.mongodb["Currency"]["Main"]
    userdata = cluster.find_one({"id": user.id})
    if userdata is None:
        DefaultTime = self.client.DefaultTime
        users = {"id": user.id, "savings": 0, "lifespan": DefaultTime,"luck": 0, "daily": 0, "weekly": 0, "monthly": 0}
        cluster.insert_one(users)

        DefaultTimeDays = DefaultTime/86400
        em = discord.Embed(title = f"The clock is ticking {user.name}!",
                           description = f"Start using various commands to gain more time, you only have **{int(DefaultTimeDays)} days** left!",
                           color = self.client.Blue,
                           timestamp=datetime.utcnow())
        try: await user.send(embed = em)
        except discord.Forbidden: 
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
    except discord.Forbidden: 
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

async def basic_embed(self, ctx, title, description,color, footer: str=""):
    em = discord.Embed(title = title,
                       description = description,
                       color = color)
    if footer is not None:
        em.set_footer(text=footer)
    em.timestamp = datetime.utcnow()

    await ctx.reply(embed = em)