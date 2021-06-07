import discord
import random
import asyncio

from discord import Member
from discord.ext import commands
from discord.ext.commands import command

from datetime import datetime
from typing import Optional

class currency(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("currency.py Loaded!")
    
    async def cog_check(self, ctx):
        if ctx.guild is not None: return True
        if not ctx.author.bot: return True

    # tbalance
    @commands.command(aliases=['bal'])
    async def balance(self, ctx, target: Optional[Member]):
        await open_account(self, ctx)
        user = target or ctx.author
        users = self.client.currencydata.find_one({"id": str(user.id)})
        
        if target is not None:
            targets = self.client.currencydata.find_one({"id": str(target.id)})
            if targets is None:
                em = discord.Embed(description = f"<:danger:848526668024250408> User doesn't exist in my database.",
                                   color = self.client.Red,
                                   timestamp=datetime.utcnow())
                await ctx.reply(embed = em)
                return

        savings_amt = round(users["savings"])
        lifespan_amt = users["lifespan"]
        lifespan_amt = await calc_DHMS_left(lifespan_amt)

        result = f"**Savings:** ${savings_amt}\n**Lifespan:** {lifespan_amt}"

        em = discord.Embed(title = f"{user.name}'s balance",
                           description=result,
                           color = self.client.Yellow,
                           timestamp=datetime.utcnow())

        await ctx.reply(embed = em)

    # tprofile
    @commands.command()
    async def profile(self, ctx, target: Optional[Member]):
        await open_account(self, ctx)
        user = target or ctx.author
        users = self.client.currencydata.find_one({"id": str(user.id)})
        
        if target is not None:
            targets = self.client.currencydata.find_one({"id": str(target.id)})
            if targets is None:
                em = discord.Embed(description = f"<:danger:848526668024250408> User doesn't exist in my database.",
                                   color = self.client.Red,
                                   timestamp=datetime.utcnow())
                await ctx.reply(embed = em)
                return

        savings_amt = users["savings"]
        lifespan_amt = users["lifespan"]
        lifespan_amt = await calc_DHMS_left(lifespan_amt)

        em = discord.Embed(color = self.client.Yellow,
                           timestamp=datetime.utcnow())
        em.set_author(name=f"{user.name}'s profile", icon_url = user.avatar_url)

        result = [(f"**Luck:** 0.25"),
                  (f"**Job:** MgRonald's"),
                  (f"**Savings:** ${savings_amt}"),
                  (f"**Lifespan:** {lifespan_amt}")]

        em.add_field(name="Worth",value=f"{result[0]}\n{result[1]}\n{result[2]}\n{result[3]}",inline=True)
        
        await ctx.reply(embed = em)

    # trich
    @commands.command()
    async def rich(self, ctx, page: int=1):
        list_of_users = self.client.currencydata.find().sort("savings", -1)
        rich_string = ""
        for x in enumerate(list_of_users, 1):
            if "savings" in x:
                savings = str(x['savings'])

                if savings == "0": break
                if ctx.guild.get_member(int(x['id'])) is None: break

                richuser = await self.client.fetch_user(int(x['id']))
                rich_string += f"**${savings}** - {richuser}\n"
        if rich_string == "":
            await ctx.send("No one with money here.")
            return
        
        em = discord.Embed(color=self.client.Yellow)
        em.add_field(name=f"Richest users in **{ctx.guild.name}**", value=rich_string, inline=False)

        em.set_footer(text=f"Page: {page}")
        em.timestamp = datetime.utcnow()
        
        await ctx.send(embed=em)

    # tpray
    @commands.command()
    async def pray(self, ctx, target: Optional[Member]):
        if self.client.cooldown.count(f"{ctx.author.id}pray") == 0:
            self.client.cooldown.append(f"{ctx.author.id}pray")
        else:
            em = discord.Embed(description = f"<:danger:848526668024250408> You are on a 30 second cooldown",
                               color = self.client.Red,
                               timestamp=datetime.utcnow())
            await ctx.reply(embed = em)
            return

        user = target or ctx.author

        if target is not None:
            targets = self.client.currencydata.find_one({"id": str(target.id)})
            prayedto = f"**{target.name}**"
            if targets is None:
                em = discord.Embed(description = f"<:danger:848526668024250408> User doesn't exist in my database.",
                                   color = self.client.Red,
                                   timestamp=datetime.utcnow())
                await ctx.reply(embed = em)
                return
        else:
            prayedto = "you"

        await open_account(self, ctx)

        time = (random.randint(1,7))
        await ctx.reply(f"God has bestowed upon {prayedto} an extra **{time}** days!!")

        time_seconds = time * 86400
        users = self.client.currencydata.find_one({"id": str(user.id)})
        new_lifespan_amt = users["lifespan"] + time_seconds
        self.client.currencydata.update_one({"id":str(user.id)},{"$set":{"lifespan":new_lifespan_amt}})

        await asyncio.sleep(30)
        self.client.cooldown.remove(f"{ctx.author.id}pray")


    #twork list
    @commands.command()
    async def worklist(self, ctx):
        em = discord.Embed(title = "List of jobs",
                           colour = self.client.Yellow,
                           timestamp=datetime.utcnow())

        em.add_field(name="MgRonald's",value="aliases: Ronalds, Maccas",inline=False)

        await ctx.reply(embed = em)


    # twork
    @commands.command()
    async def work(self, ctx, job: str=None, worktimes: str="1"):
        if job == None:
            em = discord.Embed(description = "Work where?\n-Use the command `worklist` for a list of jobs",
                               colour = self.client.Yellow,
                               timestamp=datetime.utcnow())
            await ctx.reply(embed = em)
            return
        if job not in ("Ronalds","ronalds","Maccas","maccas"):
            em = discord.Embed(description = "Thats not a valid job!\n-Use the command `worklist` for a list of jobs",
                               colour = self.client.Yellow,
                               timestamp=datetime.utcnow())
            await ctx.reply(embed = em)
            return
        if worktimes not in ("max","half"):
            worktimes = int(worktimes)
        if self.client.cooldown.count(f"{ctx.author.id}work") == 0:
            self.client.cooldown.append(f"{ctx.author.id}work")
        else:
            em = discord.Embed(description = f"<:danger:848526668024250408> You are on a 7 second cooldown",
                               color = self.client.Red,
                               timestamp=datetime.utcnow())
            await ctx.reply(embed = em)
            return
        await open_account(self, ctx)
        user = ctx.author

        users = self.client.currencydata.find_one({"id": str(user.id)})

        if worktimes in ("max","half"):
            worktimescalc = users["lifespan"] / (6*3600)
            lifespan_amt = users["lifespan"] - ((6*3600) * worktimescalc)
            if lifespan_amt < 300:
                worktimescalc = worktimescalc - 1
            if worktimes == "half":
                worktimescalc = worktimescalc/2
            worktimes = int(worktimescalc)
            worktimes = int(worktimes)
        lifespan_amt = users["lifespan"] - ((6*3600) * worktimes)
        if lifespan_amt < 300:
            em = discord.Embed(description = "<:danger:848526668024250408> You will **DIE!** If you work for that long.",
                               colour = self.client.Red,
                               timestamp=datetime.utcnow())
            await ctx.reply(embed = em)
            await user_died(self, ctx)
            return
        else:
            luck = 0.25
            min = 60
            max = 111

            #calculate savings from work
            work_amt = (random.randint(min,max))
            final_work_amt = (work_amt + (work_amt * luck))
            if final_work_amt > max:
                final_work_amt = max
            final_work_amt = int(final_work_amt * int(worktimes))
            savings_amt = round(users["savings"] + final_work_amt)

            em = discord.Embed(description = f"Worked for: 6h x{worktimes}\nTotal earnings: ${final_work_amt}",
                               colour = self.client.Yellow,
                               timestamp=datetime.utcnow())
            await ctx.reply(embed = em)

            #update values to database
            self.client.currencydata.update_one({"id":str(user.id)},{"$set":{"savings":savings_amt}})
            self.client.currencydata.update_one({"id":str(user.id)},{"$set":{"lifespan":lifespan_amt}})

        await asyncio.sleep(7)
        self.client.cooldown.remove(f"{ctx.author.id}work")
    

    # tsteal
    @commands.command(aliases=['rob'])
    async def steal(self, ctx, target: Optional[Member]):
        await open_account(self, ctx)
        user = ctx.author

        if target == None:
            em = discord.Embed(description = f"<:danger:848526668024250408> No user was specified.",
                                   color = self.client.Red,
                                   timestamp=datetime.utcnow())
            await ctx.reply(embed = em)
            return
        
        users = self.client.currencydata.find_one({"id": str(user.id)})
        if users["savings"] < 1000:
            em = discord.Embed(description = f"<:danger:848526668024250408> You need a minimum of $1000 to steal from someone",
                                   color = self.client.Red,
                                   timestamp=datetime.utcnow())
            await ctx.reply(embed = em)
            return
        
        targets = self.client.currencydata.find_one({"id": str(target.id)})
        if targets is None:
                em = discord.Embed(description = f"<:danger:848526668024250408> User doesn't exist in my database.",
                                   color = self.client.Red,
                                   timestamp=datetime.utcnow())
                await ctx.reply(embed = em)
                return
        
        if target.id == self.client.user.id:
            await ctx.reply("It's not worth it, trust me.")
            return

        if target.id == user.id:
            await ctx.reply("Yeh, because that makes sense.")
            return

        if self.client.cooldown.count(f"{ctx.author.id}steal") == 0:
            self.client.cooldown.append(f"{ctx.author.id}steal")
        else: 
            em = discord.Embed(description = f"<:danger:848526668024250408> You are on a 5 minute cooldown.",
                                   color = self.client.Red,
                                   timestamp=datetime.utcnow())
            await ctx.reply(embed = em)
            return

        luck = 0.25
        # Dertermine if stealing was a success or fail
        stealing_chance = random.randint(1,100)
        final_stealing_chance = stealing_chance + (stealing_chance * luck)
        if final_stealing_chance > 60:
            # Calculate stolen ammount
            max = targets["savings"]
            random_stole_amt = random.randint(1,max)
            stole_amt = round(random_stole_amt + (random_stole_amt * luck))
            if stole_amt > max:
                stole_amt = max

            await ctx.reply(f"You stole ${stole_amt} from {target}")

            # Update user's and target's values
            savings_amt = users["savings"] + stole_amt - 1000
            target_savings_amt = targets["savings"] - stole_amt
            self.client.currencydata.update_one({"id":str(user.id)},{"$set":{"savings":savings_amt}})
            self.client.currencydata.update_one({"id":str(target.id)},{"$set":{"savings":target_savings_amt}})
        else:
            prison_sentence = 5 #days
            prison_sentence_seconds = 86400 * prison_sentence

            await ctx.reply(f"You got caught and spent {prison_sentence} days in prison")

            # Update user's values
            lifespan_amt = users["lifespan"] - prison_sentence_seconds
            if lifespan_amt < 1:
                await user_died(self, ctx)
                return
            self.client.currencydata.update_one({"id":str(user.id)},{"$set":{"lifespan":lifespan_amt}})
        
        await asyncio.sleep(300)
        self.client.cooldown.remove(f"{ctx.author.id}steal")
    


async def calc_DHMS_left(lifespan_amt):
    lifespan_amt_days = int(lifespan_amt/86400)
    lifespan_amt_hours = int((lifespan_amt - (lifespan_amt_days * 86400))/3600)
    lifespan_amt_minutes = int((lifespan_amt - (lifespan_amt_days * 86400) - (lifespan_amt_hours * 3600))/60)
    lifespan_amt_seconds = int(lifespan_amt - (lifespan_amt_days * 86400) - (lifespan_amt_hours * 3600) - (lifespan_amt_minutes * 60))

    result = []
    loopcycleint = 0
    appendcalc = [lifespan_amt_days,lifespan_amt_hours,lifespan_amt_minutes,lifespan_amt_seconds]
    for cycleint in appendcalc:
        loopcycleint = loopcycleint + 1
        if cycleint != 0:
            type = await calc_DHMS_lefttype(loopcycleint)
            result.append(f"{cycleint} {type}")

    result = ", ".join(result)
    return result

async def calc_DHMS_lefttype(loopcycleint):
    if loopcycleint == 1:
        result = "days"
    if loopcycleint == 2:
        result = "hours"
    if loopcycleint == 3:
        result = "minutes"
    if loopcycleint == 4:
        result = "seconds"
    return result

async def open_account(self, ctx):
    user = ctx.author
    userdata = self.client.currencydata.find_one({"id": str(user.id)})
    if userdata is None:
        DefaultTime = self.client.DefaultTime
        users = {"id": str(user.id), "savings": 0, "lifespan": DefaultTime}
        self.client.currencydata.insert_one(users)

        DefaultTimeDays = DefaultTime/86400
        em = discord.Embed(title = f"The clock is ticking {user.name}!",
                           description = f"Start using various commands to gain more time, you only have **{int(DefaultTimeDays)} days** left!",
                           color = self.client.Blue,
                           timestamp=datetime.utcnow())

        await ctx.author.send(embed = em)
    return True

async def user_died(self, ctx):
    await open_account(self, ctx)
    user = ctx.author
    DefaultTime = self.client.DefaultTime

    em = discord.Embed(title = f"{user} Died!.",
                   description = "-You met the end of your lifespan. \n-You lost all your items and savings. \n-You get to keep whatever was hidden in your treasure chest.",
                   color = self.client.Red,
                   timestamp=datetime.utcnow())
    await ctx.author.send(embed = em)
    lifespan_amt = DefaultTime
    savings_amt = 0
    self.client.currencydata.update_one({"id":str(user.id)},{"$set":{"savings":savings_amt}})
    self.client.currencydata.update_one({"id":str(user.id)},{"$set":{"lifespan":lifespan_amt}})
    return
#####################################################################################################################################
def setup(client):
    client.add_cog(currency(client))