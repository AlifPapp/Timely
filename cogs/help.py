import discord
import math
from discord.ext import commands
from datetime import datetime

from .functions import View_Timeout, ButtonItem, DropdownItem, user_avatar_url

client = discord.Client

class help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("help.py Loaded!")

    async def cog_check(self, ctx):
        try: 
            if not ctx.author.bot: return True
        except: pass

    # thelp
    @commands.command()
    async def help(self, ctx, command: str="currency"):
        async def help_embed(self, self2, interaction, arg):
            if self2 is not None: #Exclude first run
                try: #If button pressed
                    if str(self2.emoji) == str(self.client.Emojis['arrow_left2']):
                        arg[0] = 1
                    if str(self2.emoji) == str(self.client.Emojis['arrow_left']):
                        if arg[0] != 1: 
                            arg[0] = arg[0] - 1
                    if str(self2.emoji) == str(self.client.Emojis['arrow_right']):
                        if arg[0] != arg[1]: 
                            arg[0] = arg[0] + 1
                    if str(self2.emoji) == str(self.client.Emojis['arrow_right2']):
                        arg[0] = arg[1]
                except: #If dropdown pressed
                    arg[0] = 1
                    arg[1] = math.ceil(len(self.client.HelpInfo[str(self2.values[0]).lower()])/8)
                    arg[2] = str(self2.values[0]).lower()
                    arg[3] = []
                    for x in self.client.HelpInfo[arg[2]]: arg[3].append(x)
                    arg[3] = sorted(arg[3])
            description = f"\n• If you need help with a command, do `{p}help <command>`."
            description += f"\n• If you have any questions/queries feel free to join the [support server](https://discord.gg/E8DnTgMvMW)\n"
            for x in arg[3][((arg[0]*8) - 8):(arg[0]*8)]: 
                description += f"\n**[{x}]({self.client.youtube})**\n{self.client.Emojis['reply_2']}{self.client.HelpInfo[arg[2]][x]['desc_short']}"
            em = discord.Embed(title = "Timely Help",
                               description = description,
                               colour = self.client.Blue)
            em.set_footer(text=f"{p}help <command> to see more details－Page {arg[0]} of {arg[1]}")
            
            if interaction is not None: await interaction.response.edit_message(embed=em)
            else: view.message = await ctx.reply(embed=em, mention_author = False, view = view)
            return arg
        def create_arg(self, category):
            cag_cmds = []
            for x in self.client.HelpInfo[category]: cag_cmds.append(x)
            cag_cmds = sorted(cag_cmds)
            arg = [1, math.ceil(len(self.client.HelpInfo[category])/8), category, cag_cmds]
            return arg
        
        categories = []
        for x in self.client.HelpInfo: categories.append(str(x).title())
        categories = sorted(categories)
        command = str(command).lower()
        p = self.client.serverprefix
        cmd = False
        if command in categories:
            arg = create_arg(self, command)
        else: # check if its an actual command
            for c in categories:
                c = c.lower()
                for x in self.client.HelpInfo[c]: 
                    if command == x: #Check is a command
                        cmd = c
                        break
                    else: #Check if is an aliase
                        if command in self.client.HelpInfo[c][x]['aliases'].split(', '):
                            command = x
                            cmd = c
                            break
            if cmd == False: 
                arg = create_arg(self, "currency")
        
        if cmd == False:
            view = View_Timeout(10)
            view.add_item(DropdownItem(self, 'Browse Commands', 1, 1, categories, help_embed, arg))
            view.add_item(ButtonItem(self, f"{self.client.Emojis['arrow_left2']}", help_embed, arg))
            view.add_item(ButtonItem(self, f"{self.client.Emojis['arrow_left']}", help_embed, arg))
            view.add_item(ButtonItem(self, f"{self.client.Emojis['arrow_right']}", help_embed, arg))
            view.add_item(ButtonItem(self, f"{self.client.Emojis['arrow_right2']}", help_embed, arg))
            await help_embed(self, None, None, arg)
            return
        em = discord.Embed(title = f"{command.capitalize()}",
                           description = f"**Description:**\n{self.client.HelpInfo[cmd][command]['desc_long']}",
                           colour = self.client.Blue,
                           timestamp=datetime.utcnow())
        em.add_field(name="**Usage:**",value=f"`{p}{self.client.HelpInfo[cmd][command]['usage']}`", inline=False)
        em.add_field(name="**Aliases:**",value=f"{self.client.HelpInfo[cmd][command]['aliases']}", inline=False)
        try: em.add_field(name="**Cooldown:**",value=f"{self.client.HelpInfo[cmd][command]['cooldown']}", inline=False)
        except: pass
        em.set_footer(text="Requested by {}".format(ctx.author.name), icon_url = user_avatar_url(ctx.author))
        await ctx.reply(embed=em, mention_author=False)

#####################################################################################################################################
def setup(client):
    client.add_cog(help(client))
