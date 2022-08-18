import discord
from discord.ext import commands
import motor.motor_asyncio as mongodb

class JoinToCreateVc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.connection = mongodb.AsyncIOMotorClient("mongodb+srv://hacker:chetan2004@cluster0.rxh8r.mongodb.net/Flame?retryWrites=true&w=majority")
        self.db = self.connection["Zeon"]["servers"]

    """JoinToCreateVc commands"""  

    def help_custom(self):
		      emoji = '<a:RA_boxingheart2:958709966368297022>'
		      label = "JoinToCreateVc"
		      description = "Shows all JoinTOCReateVc commands"
		      return emoji, label, description    
    
    @commands.Cog.listener()
    async def on_voice_state_update(self, before, after):
      if before.member.bot:
          return
      data = await self.db.find_one({"guild": before.guild.id})
      if data["joinvc"]["enabled"]== False:
          return
      else:  
        channel = data["joinvc"]["channelid"]
        if channel == None:
          return
        else:
          if before.channel is None and after.channel is not None and before.channel.id == channel:
            createChannel = await before.guild.create_voice_channel(after.member.name + '\'s channel', overwrites=[(after.guild.default_role, discord.PermissionOverwrite(connect=False)), (after.member, discord.PermissionOverwrite(connect=True))])
            await after.member.move_to(createChannel)

    @commands.group(name='jointocreate')
    async def j2c(self, ctx: commands.Context):
        """Jointocreate setup"""
        await ctx.send(f'Join To create Vc is under construction.')
    
    @j2c.command()
    async def setup(self, ctx: commands.Context):
        channel = ctx.author.voice.channel
        if not channel:
            await ctx.send(f'You must be in a voice channel to use this command.')
            return
        else:
            await self.db.update_one(
                {
                    "guild": ctx.guild.id
                },
                {
                    "$set": {
                        "joinvc.enabled" : True
                    }
                }
            )
            await self.db.update_one(
                {
                    "guild": ctx.guild.id
                },
                {
                    "$set": {
                        "joinvc.channelid" : channel.id
                    }
                }
            )
          
            await ctx.send(f'<:Tick:958955009855336558> | Set {channel.mention} to Join to create channel.')

def setup(bot):
    bot.add_cog(JoinToCreateVc(bot))