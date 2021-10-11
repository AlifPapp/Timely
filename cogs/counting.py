import asyncio
import discord
import json

from discord.ext import commands
from discord import Webhook
from datetime import datetime
from typing import Optional
from discord import Member

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

    # tsetupcounting
    @commands.command()
    async def setupcounting(self, ctx):
        if not ctx.author.guild_permissions.administrator:
            await ctx.reply(embed = await basic_embed(f"", f"{self.client.Emojis['danger']} You are missing the permission `administrator`.",self.client.Red,""))
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
                        f"{self.client.Emojis['info']}Please reply with the desired **channel**."]
        response_timeout = f"{self.client.Emojis['danger']}Setup canceled.\nTook to long to provide the required information."
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
                    embed_field1[5] = f"{self.client.Emojis['danger']}Removement of counting from {channel.mention} is canceled."
                    await message.edit(embed = await basic_embed(f"", f"{embed_field1[0]}\n \n{embed_field1[1]}\n{embed_field1[2]}\n{embed_field1[3]}\n{embed_field1[4]}\n \n{embed_field1[5]}",self.client.Blue,f""))
                    return
                embed_field1[0] = f"<:static_cog:862507223062151168>**Counting Setup**"
                embed_field1[5] = f"{self.client.Emojis['info']}Counting in {channel.mention} has been removed."
                await message.edit(embed = await basic_embed(f"", f"{embed_field1[0]}\n \n{embed_field1[1]}\n{embed_field1[2]}\n{embed_field1[3]}\n{embed_field1[4]}\n \n{embed_field1[5]}",self.client.Blue,f""))
                cluster.delete_one({"channel": channel.id})
                return
            await response.delete()

        #Starting number
        embed_field1[1] = f"<:marked_checkbox:861590371162652692> Channel: {channel.mention}"
        embed_field1[5] = f"{self.client.Emojis['info']}Please reply with the desired **starting number**."
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
        embed_field1[5] = f"{self.client.Emojis['info']}Please reply with the desired **Interval**."
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
        embed_field1[5] = f"{self.client.Emojis['info']}Please reply for **Alternate** with `[True/False]`."
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

        # Check if it is the correct channel
        if channels is None: return
        # Check if its a bot
        if user.bot:
            # Filter out webhook from actualy bots
            if user not in list(filter(lambda m: m.bot, ctx.guild.members)):
                return
        
        new_number = channels["number"] + channels["interval"]
        # Check if its the correct number
        if ctx.content != str(new_number):
            await ctx.delete()
            return
        # Check if user was previous user
        if channels["alternate"] == "True":
            if channels["last_user"] == user.id:
                await ctx.delete()
                return

        #Delete original message
        await ctx.delete()
        
        # Get webhook
        webhook = ""
        found_webhook = False
        for x in await ctx.channel.webhooks():
            if x.user == self.client.user:
                webhook = x
                found_webhook = True
                break
        if found_webhook == False:
            webhook = await ctx.channel.create_webhook(name=self.client.user, avatar=None, reason=None)
        
        #update values for main
        cluster.update_one({"channel":channel.id},{"$set":{"number":new_number}})
        cluster.update_one({"channel":channel.id},{"$set":{"last_user":user.id}})
        
        #update values for user
        cluster = self.client.mongodb["Counting"]["User"]
        users = cluster.find_one({"id": user.id})
        if users is None:
            users = {"id": user.id, "count": 1, "fonts": "default", "font": "default"}
            cluster.insert_one(users)
        cluster.update_one({"id": user.id},{"$set":{"count":users["count"]+1}})

        # Send webhook
        await webhook.send(content=f'{await convert_num2emoji(self, new_number, users["font"])}', username=f"{ctx.author}", avatar_url=ctx.author.avatar.url)

    # tcountshop
    @commands.command()
    async def countshop(self, ctx, page: int=1):
        page = 1
        data = self.client.Count_Emojis
        em = discord.Embed(title="<:count:862882885916033054> Counting Font Shop",
                           color=self.client.Blue)

        name = "Blob"
        emojis = f'{data[name]["Emoji_0"]}{data[name]["Emoji_1"]}{data[name]["Emoji_2"]}{data[name]["Emoji_3"]}{data[name]["Emoji_4"]}{data[name]["Emoji_5"]}{data[name]["Emoji_6"]}{data[name]["Emoji_7"]}{data[name]["Emoji_8"]}{data[name]["Emoji_9"]}'
        em.add_field(name=f"『{data[name]['Emoji_gif']}』 {name} +{data[name]['Cost']}", value=emojis, inline=False)

        name = "Cookie"
        emojis = f'{data[name]["Emoji_0"]}{data[name]["Emoji_1"]}{data[name]["Emoji_2"]}{data[name]["Emoji_3"]}{data[name]["Emoji_4"]}{data[name]["Emoji_5"]}{data[name]["Emoji_6"]}{data[name]["Emoji_7"]}{data[name]["Emoji_8"]}{data[name]["Emoji_9"]}'
        em.add_field(name=f"『{data[name]['Emoji_gif']}』 {name} +{data[name]['Cost']}", value=emojis, inline=False)

        name = "Tropical"
        emojis = f'{data[name]["Emoji_0"]}{data[name]["Emoji_1"]}{data[name]["Emoji_2"]}{data[name]["Emoji_3"]}{data[name]["Emoji_4"]}{data[name]["Emoji_5"]}{data[name]["Emoji_6"]}{data[name]["Emoji_7"]}{data[name]["Emoji_8"]}{data[name]["Emoji_9"]}'
        em.add_field(name=f"『{data[name]['Emoji_gif']}』 {name} +{data[name]['Cost']}", value=emojis, inline=False)

        name = "Magenta"
        emojis = f'{data[name]["Emoji_0"]}{data[name]["Emoji_1"]}{data[name]["Emoji_2"]}{data[name]["Emoji_3"]}{data[name]["Emoji_4"]}{data[name]["Emoji_5"]}{data[name]["Emoji_6"]}{data[name]["Emoji_7"]}{data[name]["Emoji_8"]}{data[name]["Emoji_9"]}'
        em.add_field(name=f"『{data[name]['Emoji_gif']}』 {name} +{data[name]['Cost']}", value=emojis, inline=False)

        name = "White"
        emojis = f'{data[name]["Emoji_0"]}{data[name]["Emoji_1"]}{data[name]["Emoji_2"]}{data[name]["Emoji_3"]}{data[name]["Emoji_4"]}{data[name]["Emoji_5"]}{data[name]["Emoji_6"]}{data[name]["Emoji_7"]}{data[name]["Emoji_8"]}{data[name]["Emoji_9"]}'
        em.add_field(name=f"『{data[name]['Emoji_gif']}』 {name} +{data[name]['Cost']}", value=emojis, inline=False)
       
        em.set_footer(text=f"Page: {page}")
        em.timestamp = datetime.utcnow()

        await ctx.send(embed=em)

    # tcount <user>
    @commands.command()
    async def count(self, ctx, target: Optional[Member]):
        cluster = self.client.mongodb["Counting"]["User"]
        user = target or ctx.author
        users = cluster.find_one({"id": user.id})
        
        if users is None: 
            count_amt = 0
            fonts = "None"
        else: 
            count_amt = users["count"]
            data = self.client.Count_Emojis
            font = users["fonts"].split()
            fonts = ""
            for x in font: 
                if x != "default": 
                    fonts += data[x]['Emoji_gif']
            if fonts == "": fonts = "None"

        result = f"**Count:** +{count_amt}\n **Fonts:** {fonts}"
        em = discord.Embed(description=result,
                           color = self.client.Blue,
                           timestamp=datetime.utcnow())
        em.set_author(name=f"{user.name}'s count", icon_url = user.avatar.url)
        await ctx.reply(embed = em)

    # tcountbuy <font>
    @commands.command()
    async def countbuy(self, ctx, font: str="None"):
        command_syntax = f"Syntax: {self.client.serverprefix}countbuy <font>"
        font = font.capitalize() 
        if font not in ("Cookie","Blob","Tropical","White","Magenta"):
            await ctx.reply(embed = await basic_embed("", f"{self.client.Emojis['danger']} Not an existing font.",self.client.Red,f"{command_syntax}"))
            return
        
        cluster = self.client.mongodb["Counting"]["User"]
        users = cluster.find_one({"id": ctx.author.id})
        
        if users is None: 
            await ctx.reply(embed = await basic_embed("", f"{self.client.Emojis['danger']} Insufficient balance.",self.client.Red,f"{command_syntax}"))
            return
        if font in users["fonts"].split():
            await ctx.reply(embed = await basic_embed("", f"{self.client.Emojis['danger']} You already have this font.",self.client.Red,f"{command_syntax}"))
            return
        
        data = self.client.Count_Emojis
        if int(users["count"]) >= int(data[font]['Cost']):
            new_count_amt = int(users["count"]) - int(data[font]['Cost'])
            cluster.update_one({"id": ctx.author.id},{"$set":{"count": new_count_amt}})
            cluster.update_one({"id": ctx.author.id},{"$set":{"fonts": f"{users['fonts']} {font}"}})
            await ctx.reply(embed = await basic_embed("Purchased", f"{ctx.author.mention} bought **{font}**\n**New count:** +{new_count_amt}",self.client.Blue,f"{command_syntax}"))
        else:
            await ctx.reply(embed = await basic_embed("", f"{self.client.Emojis['danger']} Insufficient balance.",self.client.Red,f"{command_syntax}"))

    # tcountuse <font>
    @commands.command()
    async def countuse(self, ctx, font: str="None"):
        command_syntax = f"Syntax: {self.client.serverprefix}countuse <font>"
        font = font.capitalize() 
        if font not in ("Cookie","Blob","Tropical","White","Magenta"):
            await ctx.reply(embed = await basic_embed("", f"{self.client.Emojis['danger']} Not an existing font.",self.client.Red,f"{command_syntax}"))
            return
        
        cluster = self.client.mongodb["Counting"]["User"]
        users = cluster.find_one({"id": ctx.author.id})

        if users is None: 
            await ctx.reply(embed = await basic_embed("", f"{self.client.Emojis['danger']} You don't have this font.",self.client.Red,f"{command_syntax}"))
            return
        if font in users["fonts"].split():
            cluster.update_one({"id": ctx.author.id},{"$set":{"font": font}})
            data = self.client.Count_Emojis
            emojis = f'{data[font]["Emoji_0"]}{data[font]["Emoji_1"]}{data[font]["Emoji_2"]}{data[font]["Emoji_3"]}{data[font]["Emoji_4"]}{data[font]["Emoji_5"]}{data[font]["Emoji_6"]}{data[font]["Emoji_7"]}{data[font]["Emoji_8"]}{data[font]["Emoji_9"]}'
            await ctx.reply(embed = await basic_embed("Equipped!", f"Your now using **{font} Font**\n{emojis}",self.client.Blue,f"{command_syntax}"))
        else:
            await ctx.reply(embed = await basic_embed("", f"{self.client.Emojis['danger']} You don't have this font.",self.client.Red,f"{command_syntax}"))


#####################################################################################################################################
async def convert_num2emoji(self, number,emoji):
    if emoji == "default": return number
    data = self.client.Count_Emojis
    output = ""
    for x in str(number):
        output += data[emoji][f'Emoji_{x}']
    return output

#####################################################################################################################################
def setup(client):
    client.add_cog(counting(client))
