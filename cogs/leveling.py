import discord
from discord.ext import commands
import json

class Leveling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Level commands"""
  
    def help_custom(self):
		      emoji = '<a:black_infinity:958722697280487426>'
		      label = "Level"
		      description = "Shows all Level Commands"
		      return emoji, label, description  

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # Check if the message is from a bot
        if message.author.bot:
            return
        with open('./data/databases/leveling.json', 'r') as f:
            leveling = json.load(f)
        
        # Check if the user is in the leveling database
        if str(message.author.id) not in leveling:
            leveling[str(message.author.id)] = {
                'level': 1,
                'xp': 0,
                'total_xp': 0
            }
            with open('./data/databases/leveling.json', 'w') as f:
                json.dump(leveling, f)
        
        # Check if the user has leveled up
        if leveling[str(message.author.id)]['xp'] >= leveling[str(message.author.id)]['level'] * 100:
            leveling[str(message.author.id)]['level'] += 1
            leveling[str(message.author.id)]['xp'] = 0
            leveling[str(message.author.id)]['total_xp'] += leveling[str(message.author.id)]['level'] * 100
            with open('./data/databases/leveling.json', 'w') as f:
                json.dump(leveling, f)
            channel = self.bot.get_channel(int(leveling[str(message.guild.id)]['channel']))
            await channel.send(f'{message.author.mention} has leveled up to level {leveling[str(message.author.id)]["level"]}!')

    # now make a command where the server owner can change the channel for leveling.
    @commands.group()
    async def leveling(self, ctx: commands.Context):
        await ctx.send('leveling is under construction.')
    
    @leveling.command()
    async def channel(self, ctx: commands.Context, channel: discord.TextChannel):
        if ctx.guild.owner:
            with open('./data/databases/leveling.json', 'r') as f:
                leveling = json.load(f)
            leveling[str(ctx.guild.id)]['channel'] = channel.id
            with open('./data/databases/leveling.json', 'w') as f:
                json.dump(leveling, f)
            await ctx.send(f'The channel for leveling has been set to {channel.mention}.')
    
    @commands.command()
    async def level(self, ctx: commands.Context, user: discord.Member):
        with open('./data/databases/leveling.json', 'r') as f:
            leveling = json.load(f)
        await ctx.send(f'{user.mention} is currently level {leveling[str(user.id)]["level"]}.')

def setup(bot):
    bot.add_cog(Leveling(bot))