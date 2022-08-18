import random
import discord
from discord.ext import commands
from .utils.config import *
from discord.ui import Button, View
from discord.enums import ButtonStyle

class Buttons(View):
    def __init__(self):
        super().__init__(timeout=100)

        button1 = Button(label=f'Get Floater', style=ButtonStyle.url, url='https://discord.com/oauth2/authorize?client_id=958980124198453258&permissions=8&scope=bot', emoji='<:invite:932178482451062784>')
        button2 = Button(label=f'Support Server', style=ButtonStyle.url, url='https://dsc.gg/slansic-support', emoji='<:support:932178653008248903>')
        button3 = Button(label=f'Vote me!', style=ButtonStyle.url, url='https://top.gg/bot/888799185623736350/vote', emoji='<:vote:932178725053816882>')
        button4 = Button(label=f'Partner Bot', style=ButtonStyle.url, url='https://discord.com/oauth2/authorize?client_id=958980124198453258&permissions=8&scope=bot', emoji='<:Flantic:936151853446615070>')

        self.add_item(button1)
        self.add_item(button2)
        self.add_item(button3)
        self.add_item(button4)
        self.items = [button1, button2, button3, button4]
    
    async def on_timeout(self):
        self.items[0].disabled = True
        self.items[1].disabled = True
        self.items[2].disabled = True
        self.items[3].disabled = True

class utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases=['nick'])
    @commands.has_permissions(manage_nicknames=True)
    async def changenickname(self, ctx, member: discord.Member, * , nick):
        await member.edit(nick=nick)
        await ctx.send("<a:chr_greentick:958707859649093703> | Successfully changed nickname")

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, seconds: int):
        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.send(f"<a:chr_greentick:958707859649093703> | This channel's slowmode has been set to {seconds}")

    @commands.command(aliases=['l'])
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await ctx.send(f"<a:chr_greentick:958707859649093703> | {ctx.channel.mention} has been locked!")
        if ctx.channel.permissions_for(ctx.guild.default_role).send_messages == False:
            await ctx.send("This chnanel is already locked.")

    @commands.command(aliases=['unl'])
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx: commands.Context):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
        await ctx.send(f"<a:chr_greentick:958707859649093703> | {ctx.channel.mention} has been unlocked!")
        if ctx.channel.permissions_for(ctx.guild.default_role).send_messages == True:
            await ctx.send("This channel is already unlocked.")



def setup(bot):
    bot.add_cog(utils(bot))