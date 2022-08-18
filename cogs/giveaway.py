import discord
from discord.ext import commands
import asyncio
import datetime
import random
from .utils.config import *


def convert(time):
    pos = ["s","m","h","d"]

    time_dict = {"s" : 1, "m" : 60, "h" : 3600 , "d" : 3600*24}

    unit = time[-1]

    if unit not in pos:
        return -1
    try:
        val = int(time[:-1])
    except:
        return -2


    return val * time_dict[unit]

class giveaway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Giveaway commands"""  

    def help_custom(self):
		      emoji = '<a:CV_a_giveaway:958709483289346058>'
		      label = "Giveaway"
		      description = "Shows all Giveaway commands"
		      return emoji, label, description    

    @commands.command()
    async def gstart(self, ctx):
        await ctx.send("Let's start with this giveaway! Answer these questions within 15 seconds!")

        embed=discord.Embed(title=f":tada:Giveaway Setup  • (1/3)", description=f"`Which channel should it be hosted in?`", color = DEFAULT_COLOR)
        embed2=discord.Embed(title=f":tada:Giveaway Setup  • (2/3)", description=f"`What should be the duration of the giveaway? (s|m|h|d)`", color = DEFAULT_COLOR)
        embed3=discord.Embed(title=f":tada:Giveaway Setup  • (3/3)", description=f"`What is the prize of the giveaway?`", color = DEFAULT_COLOR)


        questions = [embed, embed2, embed3]

        answers = []

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        for i in questions:
            await ctx.send(embed=i)

            try:
                msg = await self.bot.wait_for('message', timeout=15.0, check=check)
            except asyncio.TimeoutError:
                await ctx.send('You didn\'t answer in time, please be quicker next time!')
                return
            else:
                answers.append(msg.content)

        try:
            c_id = int(answers[0][2:-1])
        except:
            await ctx.send(f"You didn't mention a channel properly. Do it like this {ctx.channel.mention} next time.")
            return

        channel = self.bot.get_channel(c_id)

        time = convert(answers[1])
        if time == -1:
            await ctx.send(f"You didn't answer the time with a proper unit. Use (s|m|h|d) next time!")
            return
        elif time == -2:
            await ctx.send(f"The time must be an integer. Please enter an integer next time")
            return            

        prize = answers[2]

        await ctx.send(f"The Giveaway will be in {channel.mention} and will last {answers[1]}!")


        embed = discord.Embed(title = f":gift:{prize}", description=f"React with :tada: to enter!\n Ends: {answers[1]}\n Hosted by: {ctx.author.mention}", color = DEFAULT_COLOR)
        embed.set_footer(text = f"Ends {answers[1]} from now!")
        my_msg = await channel.send(f"**GIVEAWAY**",embed = embed)


        await my_msg.add_reaction("🎉")


        await asyncio.sleep(time)


        new_msg = await channel.fetch_message(my_msg.id)


        users = await new_msg.reactions[0].users().flatten()
        users.pop(users.index(self.bot.user))

        winner = random.choice(users)

        await my_msg.reply(f"**Congratulations**{winner.mention}!", embed=discord.Embed(description=f"You won {prize}!", color = DEFAULT_COLOR))
        await my_msg.edit(f"**GIVEAWAY ENDED**", embedend=discord.Embed(title=f":gift:{prize}", description=f"WInner: {winner.mention}\n Hosted by: {ctx.author.mention}", color = DEFAULT_COLOR))

    @commands.command()
    async def greroll(self, ctx, channel : discord.TextChannel, id_ : int):
        try:
            new_msg = await channel.fetch_message(id_)
        except:
            await ctx.send("The id was entered incorrectly.")
            return
        
        users = await new_msg.reactions[0].users().flatten()
        users.pop(users.index(self.bot.user))

        winner = random.choice(users)

        await channel.send(f"Congratulations! The new winner is {winner.mention}.!")


def setup(bot):
    bot.add_cog(giveaway(bot))