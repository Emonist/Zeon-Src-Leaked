import discord
from discord.ext import commands
from discord.utils import get
from .utils.config import *
import motor.motor_asyncio as mongodb

class VcRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.connection = mongodb.AsyncIOMotorClient("mongodb+srv://hacker:chetan2004@cluster0.rxh8r.mongodb.net/Flame?retryWrites=true&w=majority")
        self.db = self.connection["Zeon"]["servers"]

    """VcRoles commands"""

    def help_custom(self):
		      emoji = '<:announcements:958708398898184242>'
		      label = "Vc Roles"
		      description = "Shows all VcRoles Commands"
		      return emoji, label, description   

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        try:
          data = await self.db.find_one({"guild": member.guild.id})
          if data["vcrole"]["enabled"]== False:
            return
          else:  
            if not before.channel and after.channel:                
                x = data["vcrole"]["roleid"]
                r = get(member.guild.roles, id=x)
                await member.add_roles(r)
                  
            elif before.channel and not after.channel:
                x = data["vcrole"]["roleid"]
                r = get(member.guild.roles, id=x)
                await member.remove_roles(r)
        except Exception as e:
            print(e)


    @commands.group(name="Vcroles", description="vcroles new\nvcroles config\nvcroles delete",invoke_without_command=True, aliases=['vcroles'])
    @commands.has_permissions(administrator=True)
    async def VcRoles(self, ctx):
        """vcroles new\nvcroles config\nvcroles delete"""
        x = "."
        await ctx.send(f"Avaliable Commands: `{x}vcroles new <role>`, `{x}vcroles [show|config]`")

    @VcRoles.command()
    @commands.has_permissions(administrator=True)
    async def new(self, ctx, r: discord.Role):
        try:
            await self.db.update_one(
                {
                    "guild": ctx.guild.id
                },
                {
                    "$set": {
                        "vcrole.enabled" : True
                    }
                }
            )
            await self.db.update_one(
                {
                    "guild": ctx.guild.id
                },
                {
                    "$set": {
                        "vcrole.roleid" : r.id
                    }
                }
            )
            await ctx.send(f"<:Tick:958955009855336558> | Vc Roles Updated to `{r.name}`")
        except Exception as e:
            return await ctx.send(f"An error occoured {e}")

    @VcRoles.command(aliases=['show'])
    @commands.has_permissions(administrator=True)
    async def config(self, ctx):
            data = await self.db.find_one({"guild": ctx.guild.id})
            x = data["vcrole"]["roleid"]
            embed = discord.Embed(title=f"VcRoles:", description=f"<@&{x}>", color = DEFAULT_COLOR)
            await ctx.send(embed=embed)

    @VcRoles.command()
    @commands.has_permissions(administrator=True)
    async def delete(self, ctx: commands.Context):
        await self.db.update_one(
                {
                    "guild": ctx.guild.id
                },
                {
                    "$set": {
                        "vcrole.roleid" : None
                    }
                }
            )
        await ctx.send(f"<:Tick:958955009855336558> | Successfully Deleted Vc Role")


def setup(bot):
    bot.add_cog(VcRoles(bot))