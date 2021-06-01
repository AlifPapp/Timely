import asyncio
import discord
import youtube_dl
from discord.ext import commands
from datetime import datetime

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=1):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class music2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("music.py Loaded!")

    async def cog_check(self, ctx):
        if ctx.guild is not None: return True
        if not ctx.author.bot: return True

    #tplay
    @commands.command(aliases=['sing'])
    async def play(self, ctx, *, url):
        async with ctx.typing():
            if ctx.voice_client is None:
                if ctx.author.voice:
                    await ctx.author.voice.channel.connect()
                else:
                    await ctx.send("You are not connected to a voice channel.")
                    em = discord.Embed(description = f"<:danger:848526668024250408>  You are not connected to a voice channel",
                                       color = self.client.Red,
                                       timestamp=datetime.utcnow())
                    await ctx.reply(embed = em)
                    return
            elif ctx.voice_client.is_playing():
                ctx.voice_client.stop()

            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

            await ctx.send('**Now playing:** {}'.format(player.title))

            ##Cut length to 32
            #nick = "Playing: {}".format(player.title)
            #output_nick = ""
            #forloop_cycle = 0
            #for x in nick:
            #    forloop_cycle = forloop_cycle + 1
            #    output_nick += x
            #    if forloop_cycle == 32:
            #        await ctx.guild.me.edit(nick=output_nick)
            #        return


    #tpause
    @commands.command(aliases=['stop'])
    async def pause(self, ctx):
        ctx.voice_client.pause()
    
    #tresume
    @commands.command()
    async def resume(self, ctx):
        ctx.voice_client.resume()

    #tleave
    @commands.command()
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()

    #tjoin
    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice is None or ctx.author.voice.channel is None:
            em = discord.Embed(description = f"<:danger:848526668024250408> You are not connected to a voice channel",
                               color = self.client.Red,
                               timestamp=datetime.utcnow())
            await ctx.reply(embed = em)
            return

        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            vc = await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)
            vc = ctx.voice_client

async def change_botnick(self, ctx, nick: str="restore"):
    if nick == "restore":
        await ctx.guild.me.edit(nick="servernick_original")
    else:
        servernick_original = self.display_name
        await ctx.guild.me.edit(nick=nick)
    return

#####################################################################################################################################
def setup(bot):
    bot.add_cog(music2(bot))