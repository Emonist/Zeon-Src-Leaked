import discord
from discord.ext import commands
from .utils.config import *

class errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
      if isinstance(error, commands.MissingRequiredArgument):
        missing = ", ".join(error.args)
        await ctx.send(f"<a:Warn:958738005076619324> | {missing}", delete_after=10)
      elif isinstance(error, commands.MissingPermissions):
        missing_perms = ", ".join(error.missing_perms)
        await ctx.send(f"<a:Warn:958738005076619324> | You don't have the {missing_perms} permisisons to run the **{ctx.command.name}** command!", delete_after=10)
      elif isinstance(error, commands.MemberNotFound):
          await ctx.send(f"<a:Warn:958738005076619324> | Please provide a member!", delete_after=10)
      elif isinstance(error, commands.NSFWChannelRequired):
        em6 = discord.Embed(description=f"<a:Warn:958738005076619324> | Please first enable NSFW Channel in this channel!", color = discord.Colour.dark_red(), timestamp=ctx.message.created_at)
        em6.set_image(url=f"https://i.imgur.com/oe4iK5i.gif")

        await ctx.send(embed=em6, delete_after=10)
      elif isinstance(error, commands.BotMissingPermissions):
        missing = ", ".join(error.missing_perms)
        await ctx.send(f'<a:Warn:958738005076619324> | I need the **{missing}** to run the **{ctx.command.name}** command!', delete_after=10)
      elif isinstance(error, commands.CommandNotFound):
        print(" ")
      else:
        raise error

    @commands.Cog.listener()
    async def on_message(self, message):
        x = "."
        owner = self.bot.get_user(self.bot.owner_ids[0])
        if str(self.bot.user.id) in message.content:
            embed = discord.Embed(title='Hey!', description=f'I am **{self.bot.user.name}**\n • [Get {self.bot.user.name}](https://dsc.gg/flamer) | [Support Server](https://discord.gg/VzCyVjGK69)\n • The prefix for me in this server is: {x}\n • Type `{x}help` for more info.', color=DEFAULT_COLOR)
            embed.set_author(name=f'{owner.name}#{owner.discriminator}', icon_url=f'{owner.avatar}')
            await message.channel.send(embed=embed)

def setup(bot):
    bot.add_cog(errors(bot))