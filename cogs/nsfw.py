from discord.ext import commands

from .functions import basic_embed, send_redditpost

class nsfw(commands.Cog):
    def __init__(self, client):
        self.client = client
        

    @commands.Cog.listener()
    async def on_ready(self):
        print("nsfw.py Loaded!")
    
    async def cog_check(self, ctx):
        if ctx.guild is not None: return True
        if not ctx.author.bot: return True

    @commands.command()
    async def ass(self, ctx):
        if ctx.channel.is_nsfw(): await send_redditpost(self, ctx, "ass", 50)
        else: await ctx.reply(embed = await basic_embed(f"", f"<:danger:848526668024250408> Prohibited not a nsfw channel.",self.client.Red,""))
    
    @commands.command()
    async def cosplaygirls(self, ctx):
        if ctx.channel.is_nsfw(): await send_redditpost(self, ctx, "cosplaygirls", 50)
        else: await ctx.reply(embed = await basic_embed(f"", f"<:danger:848526668024250408> Prohibited not a nsfw channel.",self.client.Red,""))
    
    @commands.command()
    async def hentai(self, ctx):
        if ctx.channel.is_nsfw(): await send_redditpost(self, ctx, "hentai", 50)
        else: await ctx.reply(embed = await basic_embed(f"", f"<:danger:848526668024250408> Prohibited not a nsfw channel.",self.client.Red,""))
    
    @commands.command()
    async def nsfw(self, ctx):
        if ctx.channel.is_nsfw(): await send_redditpost(self, ctx, "nsfw", 50)
        else: await ctx.reply(embed = await basic_embed(f"", f"<:danger:848526668024250408> Prohibited not a nsfw channel.",self.client.Red,""))
    
    @commands.command()
    async def Sexy(self, ctx):
        if ctx.channel.is_nsfw(): await send_redditpost(self, ctx, "Sexy", 50)
        else: await ctx.reply(embed = await basic_embed(f"", f"<:danger:848526668024250408> Prohibited not a nsfw channel.",self.client.Red,""))
    
    @commands.command()
    async def Sexy_Asians(self, ctx):
        if ctx.channel.is_nsfw(): await send_redditpost(self, ctx, "Sexy_Asians", 50)
        else: await ctx.reply(embed = await basic_embed(f"", f"<:danger:848526668024250408> Prohibited not a nsfw channel.",self.client.Red,""))
    
    @commands.command()
    async def tattooed_redheads(self, ctx):
        if ctx.channel.is_nsfw(): await send_redditpost(self, ctx, "tattooed_redheads", 50)
        else: await ctx.reply(embed = await basic_embed(f"", f"<:danger:848526668024250408> Prohibited not a nsfw channel.",self.client.Red,""))
    
    @commands.command()
    async def tattooedgirls(self, ctx):
        if ctx.channel.is_nsfw(): await send_redditpost(self, ctx, "tattooedgirls", 50)
        else: await ctx.reply(embed = await basic_embed(f"", f"<:danger:848526668024250408> Prohibited not a nsfw channel.",self.client.Red,""))
    
    @commands.command()
    async def twerking(self, ctx):
        if ctx.channel.is_nsfw(): await send_redditpost(self, ctx, "twerking", 50)
        else: await ctx.reply(embed = await basic_embed(f"", f"<:danger:848526668024250408> Prohibited not a nsfw channel.",self.client.Red,""))
        
#####################################################################################################################################
def setup(client):
    client.add_cog(nsfw(client))
