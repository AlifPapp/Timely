import asyncio
from discord.ext import commands
from discord import Webhook

from .functions import basic_embed

class counting(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("counting.py Loaded!")
    
    async def cog_check(self, ctx):
        try: 
            if ctx.guild is not None and not ctx.author.bot: return True
        except: pass

    #tsetupcounting
    @commands.command()
    async def setupcounting(self, ctx):
        if not ctx.author.guild_permissions.administrator:
            await ctx.reply(embed = await basic_embed(f"", f"<:danger:848526668024250408> You are missing the permission `administrator`.",self.client.Red,""))
            return

        #Setup Vars
        guild = ctx.guild
        channel = ctx.channel
        user = ctx.author
        cluster = self.client.mongodb["Counting"]["Main"]
        insert = False
        
        guilds = cluster.find_one({"channel": channel.id})
        if guilds is not None: #if command was sent in a counting channel
            return

        embed_field1 = [f"<a:cogs:859407226035765288> **Setting up counting.**",
                        f"<:empty_checkbox:861484710898434108> Channel: NA",
                        f"<:empty_checkbox:861484710898434108> Starting number: NA",
                        f"<:empty_checkbox:861484710898434108> Interval: NA",
                        f"<:empty_checkbox:861484710898434108> Alternate: NA",
                        f"<:info:848526617449070633>Please reply with the desired **channel**."]
        response_timeout = f"<:danger:848526668024250408>Setup canceled.\nTook to long to provide the required information."
        message = await ctx.reply(embed = await basic_embed(f"", f"{embed_field1[0]}\n \n{embed_field1[1]}\n{embed_field1[2]}\n{embed_field1[3]}\n{embed_field1[4]}\n \n{embed_field1[5]}",self.client.Blue,f"15 secconds to respond"))

        #Channel
        def check(m):
            return m.channel == ctx.channel and m.author == user and len(m.channel_mentions) != 0
        try:
            response = await self.client.wait_for('message', check=check, timeout=15)
        except asyncio.TimeoutError:
            embed_field1[0] = f"<:static_cog:862507223062151168>**Counting Setup canceled**"
            embed_field1[5] = f"{response_timeout}"
            await message.edit(embed = await basic_embed(f"", f"{embed_field1[0]}\n \n{embed_field1[1]}\n{embed_field1[2]}\n{embed_field1[3]}\n{embed_field1[4]}\n \n{embed_field1[5]}",self.client.Blue,f""))
            return
        await response.delete()
        channel = response.channel_mentions[0]

        guilds = cluster.find_one({"channel": channel.id})
        if guilds is None: insert = True
        elif channel.id == guilds["channel"]:
            embed_field1[5] = f"<:warning:861488027905425419>{channel.mention} has already been **set**.\n<:question_mark:861771749461196800>Alter settings for {channel.mention}? `[Yes/No]`"
            await message.edit(embed = await basic_embed(f"", f"{embed_field1[0]}\n \n{embed_field1[1]}\n{embed_field1[2]}\n{embed_field1[3]}\n{embed_field1[4]}\n \n{embed_field1[5]}",self.client.Blue,f"15 secconds to respond"))
            
            def check(m):
                return m.channel == ctx.channel and m.author == user and m.content in ("Yes","yes","No","no")
            try:
                response = await self.client.wait_for('message', check=check, timeout=15)
            except asyncio.TimeoutError:
                embed_field1[0] = f"<:static_cog:862507223062151168>**Counting Setup canceled**"
                embed_field1[5] = f"{response_timeout}"
                await message.edit(embed = await basic_embed(f"", f"{embed_field1[0]}\n \n{embed_field1[1]}\n{embed_field1[2]}\n{embed_field1[3]}\n{embed_field1[4]}\n \n{embed_field1[5]}",self.client.Blue,f""))
                return
            if response.content not in ("yes","Yes"):
                await response.delete()
                embed_field1[5] = f"<:question_mark:861771749461196800>Remove counting from {channel.mention}? `[Yes/No]`"
                await message.edit(embed = await basic_embed(f"", f"{embed_field1[0]}\n \n{embed_field1[1]}\n{embed_field1[2]}\n{embed_field1[3]}\n{embed_field1[4]}\n \n{embed_field1[5]}",self.client.Blue,f"15 secconds to respond"))

                def check(m):
                    return m.channel == ctx.channel and m.author == user and m.content in ("Yes","yes","No","no")
                try:
                    response = await self.client.wait_for('message', check=check, timeout=15)
                except asyncio.TimeoutError:
                    embed_field1[0] = f"<:static_cog:862507223062151168>**Counting Setup canceled**"
                    embed_field1[5] = f"{response_timeout}"
                    await message.edit(embed = await basic_embed(f"", f"{embed_field1[0]}\n \n{embed_field1[1]}\n{embed_field1[2]}\n{embed_field1[3]}\n{embed_field1[4]}\n \n{embed_field1[5]}",self.client.Blue,f""))
                    return
                if response.content not in ("yes","Yes"):
                    embed_field1[0] = f"<:static_cog:862507223062151168>**Counting Setup canceled**"
                    embed_field1[5] = f"<:danger:848526668024250408>Removement of counting from {channel.mention} is canceled."
                    await message.edit(embed = await basic_embed(f"", f"{embed_field1[0]}\n \n{embed_field1[1]}\n{embed_field1[2]}\n{embed_field1[3]}\n{embed_field1[4]}\n \n{embed_field1[5]}",self.client.Blue,f""))
                    return
                embed_field1[0] = f"<:static_cog:862507223062151168>**Counting Setup**"
                embed_field1[5] = f"<:info:848526617449070633>Counting in {channel.mention} has been removed."
                await message.edit(embed = await basic_embed(f"", f"{embed_field1[0]}\n \n{embed_field1[1]}\n{embed_field1[2]}\n{embed_field1[3]}\n{embed_field1[4]}\n \n{embed_field1[5]}",self.client.Blue,f""))
                cluster.delete_one({"channel": channel.id})
                return
            await response.delete()

        #Starting number
        embed_field1[1] = f"<:marked_checkbox:861590371162652692> Channel: {channel.mention}"
        embed_field1[5] = f"<:info:848526617449070633>Please reply with the desired **starting number**."
        await message.edit(embed = await basic_embed(f"", f"{embed_field1[0]}\n \n{embed_field1[1]}\n{embed_field1[2]}\n{embed_field1[3]}\n{embed_field1[4]}\n \n{embed_field1[5]}",self.client.Blue,f"15 secconds to respond"))

        def check(m):
            return m.channel == ctx.channel and m.author == user and m.content[1::].isdigit() and m.content[0] == "-" or m.content[0].isdigit()
        try:
            response = await self.client.wait_for('message', check=check, timeout=15)
        except asyncio.TimeoutError:
            embed_field1[0] = f"<:static_cog:862507223062151168>**Counting Setup canceled**"
            embed_field1[5] = f"{response_timeout}"
            await message.edit(embed = await basic_embed(f"", f"{embed_field1[0]}\n \n{embed_field1[1]}\n{embed_field1[2]}\n{embed_field1[3]}\n{embed_field1[4]}\n \n{embed_field1[5]}",self.client.Blue,f""))
            return
        await response.delete()
        starting_number = int(response.content)

        #Interval
        embed_field1[2] = f"<:marked_checkbox:861590371162652692> Starting number: {starting_number}"
        embed_field1[5] = f"<:info:848526617449070633>Please reply with the desired **Interval**."
        temp = f"{embed_field1[0]}\n \n{embed_field1[1]}\n{embed_field1[2]}\n{embed_field1[3]}\n{embed_field1[4]}\n \n{embed_field1[5]}"
        await message.edit(embed = await basic_embed(f"", f"{temp}",self.client.Blue,f"15 secconds to respond"))

        def check(m):
            return m.channel == ctx.channel and m.author == user and m.content[1::].isdigit() and m.content[0] == "-" or m.content[0].isdigit()
        try:
            response = await self.client.wait_for('message', check=check, timeout=15)
        except asyncio.TimeoutError:
            embed_field1[0] = f"<:static_cog:862507223062151168>**Counting Setup canceled**"
            embed_field1[5] = f"{response_timeout}"
            await message.edit(embed = await basic_embed(f"", f"{embed_field1[0]}\n \n{embed_field1[1]}\n{embed_field1[2]}\n{embed_field1[3]}\n{embed_field1[4]}\n \n{embed_field1[5]}",self.client.Blue,f""))
            return
        await response.delete()
        interval = int(response.content)

        #Alternate
        embed_field1[3] = f"<:marked_checkbox:861590371162652692> Interval: {interval}"
        embed_field1[5] = f"<:info:848526617449070633>Please reply for **Alternate** with `[True/False]`."
        temp = f"{embed_field1[0]}\n \n{embed_field1[1]}\n{embed_field1[2]}\n{embed_field1[3]}\n{embed_field1[4]}\n \n{embed_field1[5]}"
        await message.edit(embed = await basic_embed(f"", f"{temp}",self.client.Blue,f"15 secconds to respond"))

        def check(m):
            return m.channel == ctx.channel and m.author == user and m.content in ("True","False")
        try:
            response = await self.client.wait_for('message', check=check, timeout=15)
        except asyncio.TimeoutError:
            embed_field1[0] = f"<:static_cog:862507223062151168>**Counting Setup canceled**"
            embed_field1[5] = f"{response_timeout}"
            await message.edit(embed = await basic_embed(f"", f"{embed_field1[0]}\n \n{embed_field1[1]}\n{embed_field1[2]}\n{embed_field1[3]}\n{embed_field1[4]}\n \n{embed_field1[5]}",self.client.Blue,f""))
            return
        await response.delete()
        alternate = str(response.content)

        #Complete setup_edit
        embed_field1[0] = f"<:static_cog:862507223062151168>**Counting Setup**"
        embed_field1[4] = f"<:marked_checkbox:861590371162652692> Alternate: {alternate}"
        embed_field1[5] = f"<a:green_check1:861578504188198912>Setup Complete."
        temp = f"{embed_field1[0]}\n \n{embed_field1[1]}\n{embed_field1[2]}\n{embed_field1[3]}\n{embed_field1[4]}\n \n{embed_field1[5]}"
        await message.edit(embed = await basic_embed(f"", f"{temp}",self.client.Blue,f""))

        #Update or insert values to MongoDB
        if insert == True:
            guilds = {"guild": guild.id, "channel": channel.id, "number": starting_number, "interval": interval, "alternate": alternate, "last_user": user.id}
            cluster.insert_one(guilds)
        else:
            cluster.update_one({"channel":channel.id},{"$set":{"number":starting_number}})
            cluster.update_one({"channel":channel.id},{"$set":{"interval":interval}})
            cluster.update_one({"channel":channel.id},{"$set":{"alternate":alternate}})

        #Delete channel that cant be found in guild
        list_of_guild = cluster.find({"guild": guild.id})
        for x in list_of_guild:
            channel_id = x["channel"]
            found = False
            for xx in guild.channels:
                if channel_id == xx.id:
                    found = True
            if found == False:
                cluster.delete_one({"channel": channel_id})

    #on_message counting
    @commands.Cog.listener()
    async def on_message(self, ctx):
        user = ctx.author
        channel = ctx.channel
        cluster = self.client.mongodb["Counting"]["Main"]
        channels = cluster.find_one({"channel": channel.id})

        if channels is None: return
        if user.bot:
            if user not in list(filter(lambda m: m.bot, ctx.guild.members)):
                return
        
        new_number = channels["number"] + channels["interval"]
        if ctx.content != str(new_number):
            await ctx.delete()
            return
        if channels["alternate"] == "True":
            if channels["last_user"] == user.id:
                await ctx.delete()
                return

        #update values
        cluster.update_one({"channel":channel.id},{"$set":{"number":new_number}})
        cluster.update_one({"channel":channel.id},{"$set":{"last_user":user.id}})

        #send webhook
        await ctx.delete()
        webhook = ""
        found_webhook = False
        for x in await ctx.channel.webhooks():
            if x.user == self.client.user:
                webhook = x
                found_webhook = True
                break
        
        if found_webhook == False:
            webhook = await ctx.channel.create_webhook(name=self.client.user, avatar=None, reason=None)
        await webhook.send(content=f"{new_number}", username=f"{ctx.author}", avatar_url=ctx.author.avatar.url)




#####################################################################################################################################
def setup(client):
    client.add_cog(counting(client))