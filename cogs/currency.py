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

    # tbalance <user>
    @commands.command(aliases=['bal'])
    async def balance(self, ctx, target: Optional[Member]):
        await open_account(self, ctx)
        user = target or ctx.author
        users = self.client.currencydata.find_one({"id": str(user.id)})
        command_syntax = f"{self.client.serverprefix}balance <user>"

        if target is not None:
            targets = self.client.currencydata.find_one({"id": str(target.id)})
            if targets is None:
                await basic_embed(self, ctx,"", f"<:danger:848526668024250408> User doesn't exist in my database.\n{command_syntax}",self.client.Red,"")
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

    # tprofile <user>
    @commands.command()
    async def profile(self, ctx, target: Optional[Member]):
        await open_account(self, ctx)
        user = target or ctx.author
        users = self.client.currencydata.find_one({"id": str(user.id)})
        command_syntax = f"{self.client.serverprefix}profile <user>"

        if target is not None:
            targets = self.client.currencydata.find_one({"id": str(target.id)})
            if targets is None:
                await basic_embed(self, ctx,"", f"<:danger:848526668024250408> User doesn't exist in my database.\n{command_syntax}",self.client.Red,"")
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

    # trich <page>
    @commands.command()
    async def rich(self, ctx, page: int=1):
        page = abs(int(page))
        if page > 99: page = 99
        list_of_users = self.client.currencydata.find().sort("savings", -1)
        rich_string = ""
        cycle_int = 0
        for x in list_of_users:
            if "savings" in x:
                savings = int(x["savings"])
                if savings == 0: break
                if ctx.guild.get_member(int(x['id'])) is None: break
                cycle_int = cycle_int + 1
                
                if cycle_int > ((page*10) - ((page-1)*10)) or page == 1:
                    richuser = await self.client.fetch_user(int(x['id']))
                    rich_string += f"**${savings}** - {richuser}\n"
                if cycle_int == int(page*10): break
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
            await basic_embed(self, ctx,"", f"<:danger:848526668024250408> You are on a 30 second cooldown.",self.client.Red,"")
            return
        await open_account(self, ctx)
        time = (random.randint(1,7))

        if target is not None:
            targets = self.client.currencydata.find_one({"id": str(target.id)})
            if targets is None:
                await basic_embed(self, ctx,"", f"<:danger:848526668024250408> User doesn't exist in my database.",self.client.Red,"")
                return
            await target.send(F"{ctx.author} has prayed for your wellbeing and so God has bestowed upon you an extra **{time}** days!!")
            await ctx.reply(f"God has bestowed upon **{target.name}** an extra **{time}** days!!")
        else: 
            await ctx.reply(f"God has bestowed upon you an extra **{time}** days!!")

        target = target or ctx.author

        # update values
        time_seconds = time * 86400
        targets = self.client.currencydata.find_one({"id": str(target.id)})
        new_lifespan_amt = targets["lifespan"] + time_seconds
        self.client.currencydata.update_one({"id":str(target.id)},{"$set":{"lifespan":new_lifespan_amt}})

        await asyncio.sleep(30)
        self.client.cooldown.remove(f"{ctx.author.id}pray")

    # tdaily
    @commands.command()
    async def daily(self, ctx):
        if self.client.cooldown.count(f"{ctx.author.id}daily") == 0:
            self.client.cooldown.append(f"{ctx.author.id}daily")
        else:
            await basic_embed(self, ctx,"", f"<:danger:848526668024250408> You are on a 1 day cooldown.",self.client.Red,"")
            return
        
        await open_account(self, ctx)
        user = ctx.author
        await basic_embed(self, ctx,"Daily rewards", f"{user} claimed $100!",self.client.Yellow,"")

        # update values
        users = self.client.currencydata.find_one({"id": str(user.id)})
        new_savings_amt = users["savings"] + 100
        self.client.currencydata.update_one({"id":str(user.id)},{"$set":{"savings":new_savings_amt}})

        await asyncio.sleep(86400)
        self.client.cooldown.remove(f"{ctx.author.id}daily")

    # tweekly
    @commands.command()
    async def weekly(self, ctx):
        if self.client.cooldown.count(f"{ctx.author.id}weekly") == 0:
            self.client.cooldown.append(f"{ctx.author.id}weekly")
        else:
            await basic_embed(self, ctx,"", f"<:danger:848526668024250408> You are on a 1 week cooldown.",self.client.Red,"")
            return
        
        await open_account(self, ctx)
        user = ctx.author
        await basic_embed(self, ctx,"Weekly rewards", f"{user} claimed $1000!",self.client.Yellow,"")

        # update values
        users = self.client.currencydata.find_one({"id": str(user.id)})
        new_savings_amt = users["savings"] + 1000
        self.client.currencydata.update_one({"id":str(user.id)},{"$set":{"savings":new_savings_amt}})

        await asyncio.sleep(604800)
        self.client.cooldown.remove(f"{ctx.author.id}weekly")
    
    # tmonthly
    @commands.command()
    async def monthly(self, ctx):
        if self.client.cooldown.count(f"{ctx.author.id}monthly") == 0:
            self.client.cooldown.append(f"{ctx.author.id}monthly")
        else:
            await basic_embed(self, ctx,"", f"<:danger:848526668024250408> You are on a 1 month cooldown.",self.client.Red,"")
            return
        
        await open_account(self, ctx)
        user = ctx.author
        await basic_embed(self, ctx,"Monthly rewards", f"{user} claimed $10000!",self.client.Yellow,"")

        # update values
        users = self.client.currencydata.find_one({"id": str(user.id)})
        new_savings_amt = users["savings"] + 10000
        self.client.currencydata.update_one({"id":str(user.id)},{"$set":{"savings":new_savings_amt}})

        await asyncio.sleep(2628000)
        self.client.cooldown.remove(f"{ctx.author.id}monthly")

    #twork list
    @commands.command()
    async def worklist(self, ctx):
        em = discord.Embed(title = "List of jobs",
                           colour = self.client.Yellow,
                           timestamp=datetime.utcnow())

        em.add_field(name="MgRonald's",value="aliases: Ronalds, Maccas",inline=False)

        await ctx.reply(embed = em)

    # twork <job> <times>
    @commands.command()
    async def work(self, ctx, job: str=None, worktimes: str="1"):
        if job == None:
            await basic_embed(self, ctx,"", f"Work where?\n-Use the command `worklist` for a list of jobs.",self.client.Yellow,"")
            return
        
        if job not in ("Ronalds","ronalds","Maccas","maccas"):
            await basic_embed(self, ctx,"", f"Thats not a valid job!\n-Use the command `worklist` for a list of jobs.",self.client.Yellow,"")
            return
        
        if worktimes not in ("max","half"):
            worktimes = int(worktimes)
        if self.client.cooldown.count(f"{ctx.author.id}work") == 0:
            self.client.cooldown.append(f"{ctx.author.id}work")
        else:
            await basic_embed(self, ctx,"", f"<:danger:848526668024250408> You are on a 7 second cooldown.",self.client.Red,"")
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
        worktimes = abs(int(worktimes))

        lifespan_amt = users["lifespan"] - ((6*3600) * worktimes)
        if lifespan_amt < 300:
            await basic_embed(self, ctx,"", f"<:danger:848526668024250408> You will **DIE!** If you work for that long.",self.client.Red,"")
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
    
    # tsteal <user>
    @commands.command(aliases=['rob'])
    async def steal(self, ctx, target: Optional[Member]):
        await open_account(self, ctx)
        user = ctx.author
        command_syntax = f"Syntax: {self.client.serverprefix}steal <user>"
        
        if target == None: 
            await basic_embed(self, ctx,f"", f"<:danger:848526668024250408> No user was specified.",self.client.Red,f"{command_syntax}") 
            return
        
        users = self.client.currencydata.find_one({"id": str(user.id)})
        if users["savings"] < 1000:
            await basic_embed(self, ctx,f"", f"<:danger:848526668024250408> You need a minimum of $1000 to steal from someone.",self.client.Red,"")
            return
        
        targets = self.client.currencydata.find_one({"id": str(target.id)})
        if targets is None:
            await basic_embed(self, ctx,f"", f"<:danger:848526668024250408> User doesn't exist in my database.",self.client.Red,"")
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
            await basic_embed(self, ctx,f"", f"<:danger:848526668024250408> You are on a 5 minute cooldown.",self.client.Red,"")
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

            # Update user's and target's values
            savings_amt = users["savings"] + stole_amt - 1000
            target_savings_amt = targets["savings"] - stole_amt
            self.client.currencydata.update_one({"id":str(user.id)},{"$set":{"savings":savings_amt}})
            self.client.currencydata.update_one({"id":str(target.id)},{"$set":{"savings":target_savings_amt}})

            await ctx.reply(f"You stole **${stole_amt}** from {target}")
            await target.send(f"{ctx.author} has stolen from you **${stole_amt}**")
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
    
    #tgive <user> <amount>
    @commands.command()
    async def give(self, ctx, target: Optional[Member], ammount: str="0"):
        await open_account(self, ctx)
        user = ctx.author
        command_syntax = f"Syntax: {self.client.serverprefix}give <user> <amount>"

        if target == None:
            await basic_embed(self, ctx,f"", f"<:danger:848526668024250408> No user was specified.",self.client.Red,f"{command_syntax}")
            return
        
        if ammount == "0":
            await basic_embed(self, ctx,f"", f"<:danger:848526668024250408> No ammount was specified.",self.client.Red,f"{command_syntax}")
            return

        users = self.client.currencydata.find_one({"id": str(user.id)})
        if ammount == "half": 
            ammount = users["savings"]/2
        elif ammount == "max":
            ammount = users["savings"]
        else:
            ammount = abs(int(ammount))
        
        if users["savings"] < ammount:
            await basic_embed(self, ctx,f"", f"<:danger:848526668024250408> You don't have that much money.",self.client.Red,"")
            return

        targets = self.client.currencydata.find_one({"id": str(target.id)})
        if targets is None:
                await basic_embed(self, ctx,f"", f"<:danger:848526668024250408> User doesn't exist in my database.",self.client.Red,"")
                return
        
        if target.id == user.id:
            await ctx.reply("Yeh, because that makes sense.")
            return

        if self.client.cooldown.count(f"{ctx.author.id}give") == 0:
            self.client.cooldown.append(f"{ctx.author.id}give")
        else: 
            await basic_embed(self, ctx,f"", f"<:danger:848526668024250408> You are on a 7 second cooldown.",self.client.Red,"")
            return
        
        
        user_savings_amt = users["savings"] - ammount
        target_savings_amt = targets["savings"] + ammount
        self.client.currencydata.update_one({"id":str(user.id)},{"$set":{"savings":user_savings_amt}})
        self.client.currencydata.update_one({"id":str(target.id)},{"$set":{"savings":target_savings_amt}})

        await ctx.reply(f"You gave {target} **${ammount}**")
        await target.send(f"{ctx.author} has given you **${ammount}**")

        await asyncio.sleep(7)
        self.client.cooldown.remove(f"{ctx.author.id}give")

#####################################################################################################################################
########################################################## D E V L O P E R ##########################################################
########################################################### C O M A N D S ###########################################################
#####################################################################################################################################
    # teditusercurrency
    @commands.command()
    async def editusercurrency(self, ctx, target: Optional[Member], type: str="", edit_int: int=0):
        if ctx.author.id in self.client.developerid:
            edit_int = int(edit_int)
            command_syntax = f"<:invisible:852047285109522442> Syntax:`{self.client.serverprefix}editusercurrency <user> <type> <amount>`"
            if None in (target, type) or edit_int == 0:
                await basic_embed(self, ctx,f"", f"<:danger:848526668024250408> Incorrect args, use the example below.\n{command_syntax}",self.client.Red,"")
                return

            targets = self.client.currencydata.find_one({"id": str(target.id)})
            if targets is None:
                await basic_embed(self, ctx,f"", f"<:danger:848526668024250408> User doesn't exist in my database.",self.client.Red,"")
                return
            if type == "savings":
                target_savings_amt = targets["savings"] + edit_int
                try:
                    self.client.currencydata.update_one({"id":str(target.id)},{"$set":{"savings":target_savings_amt}})
                except OverflowError:
                    await basic_embed(self, ctx,f"", f"<:danger:848526668024250408> OverflowError.\nTry a smaller number maybe.",self.client.Red,"")
                    return
                await basic_embed(self, ctx,f"", f"<:info:848526617449070633> You successfully edited {target}'s savings by {edit_int}",self.client.Blue,"")
            elif type == "lifespan":
                target_savings_amt = targets["lifespan"] + edit_int
                try:
                    self.client.currencydata.update_one({"id":str(target.id)},{"$set":{"lifespan":target_savings_amt}})
                except OverflowError:
                    await basic_embed(self, ctx,f"", f"<:danger:848526668024250408> OverflowError.\nTry a smaller number maybe.",self.client.Red,"")
                    return
                await ctx.send(f"You successfully edited {target}'s lifespan by {edit_int}")
            else: 
                await basic_embed(self, ctx,f"", f"<:danger:848526668024250408> Incorrect type.",self.client.Red,"")
        return

async def basic_embed(self, ctx, title, description,color, footer: str=""):
    em = discord.Embed(title = title,
                       description = description,
                       color = color)
    if footer is not None:
        em.set_footer(text=footer)
    em.timestamp = datetime.utcnow()

    await ctx.reply(embed = em)

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