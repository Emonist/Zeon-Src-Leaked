import discord, json
from discord.ext import commands
from .utils.config import *
import motor.motor_asyncio as mongodb

class logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.connection = mongodb.AsyncIOMotorClient("mongodb+srv://hacker:chetan2004@cluster0.rxh8r.mongodb.net/Flame?retryWrites=true&w=majority")
        self.db = self.connection["Zeon"]["servers"]

    """Logging commands"""  

    def help_custom(self):
		      emoji = '<a:star:958708217137999902>'
		      label = "Logging"
		      description = "Shows all Logging Commands"
		      return emoji, label, description  

    @commands.group(name="logging", description="logging channel\nlogging config\nlogging delete", invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def logging(self, ctx):
        """logging channel\nlogging config\nlogging delete"""
        x = "."
        await ctx.send(f"Available Commands: `{x}logging channel`")

    @logging.command()
    @commands.has_permissions(administrator=True)
    async def channel(self, ctx, c: discord.TextChannel):
        try:
            await self.db.update_one(
                {
                    "guild": ctx.guild.id
                },
                {
                    "$set": {
                        "log-channel" : c.id
                    }
                }
            )
            await ctx.send(f"<:Tick:958955009855336558> | All logs channel are updated to <#{c.id}>")
        except Exception as e:
            return await ctx.send(f"An error occoured {e}")

    @logging.command(aliases=['show'])
    @commands.has_permissions(administrator=True)
    async def config(self, ctx):
        data = await self.db.find_one({"guild": ctx.guild.id})     
        x = data["log-channel"]
        if x == None:
          embed = discord.Embed(title=f"Logging channel:", description=f"No Logging Channel Found", color = DEFAULT_COLOR)
          await ctx.send(embed=embed)
        else:
          embed = discord.Embed(title=f"Logging channel:", description=f"<#{x}>", color = DEFAULT_COLOR)
          await ctx.send(embed=embed)

    @logging.command()
    @commands.has_permissions(administrator=True)
    async def delete(self, ctx: commands.Context):
        await self.db.update_one(
                {
                    "guild": ctx.guild.id
                },
                {
                    "$set": {
                        "log-channel" : None
                    }
                }
            )
        await ctx.send(f'<:Tick:958955009855336558> | Successfully Deleted Logging Channel')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.bot:
            return
        data = await self.db.find_one({"guild": member.guild.id})     
        x = data["log-channel"]
        if x == None:
          return
        else:  
          channel = self.bot.get_channel(x)
          member1 = int(member.created_at.timestamp())
          embed = discord.Embed(title="A member has joined the server.", description=f"{member.mention} | {member.id}\n:bust_in_silhouette: Account created at <t:{member1}:D>", color = discord.Colour.green())
          embed.set_thumbnail(url=member.avatar)
          embed.set_author(name=member.name, icon_url=member.avatar)
          embed.set_footer(text="JOIN", icon_url=self.bot.user.avatar)
          await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if member.bot:
            return
        data = await self.db.find_one({"guild": member.guild.id})     
        x = data["log-channel"]
        if x == None:
          return
        else:  
          channel = self.bot.get_channel(x)
          member1 = int(member.created_at.timestamp())
          embed = discord.Embed(title="A member is no longer in the server.", description=f"{member.name} | {member.id}\n :bust_in_silhouette: Account created at <t:{member1}:D>", color = discord.Colour.dark_red())
          embed.set_thumbnail(url=member.avatar)
          embed.set_author(name=member.name, icon_url=member.avatar)
          embed.set_footer(text="LEFT", icon_url=self.bot.user.avatar)
          await channel.send(embed=embed)

    # CHANNEL LOGGING

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        data = await self.db.find_one({"guild": channel.guild.id})     
        x = data["log-channel"]
        if x == None:
          return
        else:  
          c = self.bot.get_channel(x)
          embed = discord.Embed(description=f"New channel ({channel.mention}) has beeen Created ", color = discord.Colour.green())
          embed.add_field(name=f"Name", value=f"{channel.name} (ID: {channel.id})")
          embed.add_field(name=f"Position", value=f"{channel.position}")
          embed.set_footer(text="CHANNEL CREATE", icon_url=self.bot.user.avatar)
          await c.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        data = await self.db.find_one({"guild": channel.guild.id})     
        x = data["log-channel"]
        if x == None:
          return
        else:  
          c = self.bot.get_channel(x)
          embed = discord.Embed(description="A channel has been deleted", color = discord.Colour.dark_red())
          embed.add_field(name=f"Name", value=f"{channel.name} (ID: {channel.id})")
          embed.add_field(name=f"Position", value=f"{channel.position}")
          embed.set_footer(text="CHANNEL DELETE", icon_url=self.bot.user.avatar)
          await c.send(embed=embed)
    
    # ROLE LOGGING
    
    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        data = await self.db.find_one({"guild": role.guild.id})     
        x = data["log-channel"]
        if x == None:
          return
        else:  
          channel = self.bot.get_channel(x)
          embed = discord.Embed(description=f"New role ({role.mention}) has been Created", color = discord.Colour.green())
          embed.add_field(name="Name", value=f"{role.name} (ID: {role.id})")
          embed.add_field(name="Color", value=f"{role.colour}")
          embed.add_field(name="Postion", value=f"{role.position}")
          embed.set_footer(text="ROLE CREATE", icon_url=self.bot.user.avatar)
          await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        data = await self.db.find_one({"guild": role.guild.id})     
        x = data["log-channel"]
        if x == None:
          return
        else:  
          channel = self.bot.get_channel(x)
          embed = discord.Embed(description=f"Role ({role.mention}) has been Deleted", color = discord.Colour.dark_red())
          embed.add_field(name="Name", value=f"{role.name} (ID: {role.id})")
          embed.add_field(name="Color", value=f"{role.colour}")
          embed.add_field(name="Postion", value=f"{role.position}")
          embed.set_footer(text="ROLE DELETE", icon_url=self.bot.user.avatar)
          await channel.send(embed=embed)

    # MESSAGE LOGGGING

    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload: discord.RawMessageDeleteEvent):
        data = await self.db.find_one({"guild": payload.guild_id})     
        x = data["log-channel"]
        if x == None:
          return
        else: 
          channel = self.bot.get_channel(x)
          embed = discord.Embed(description=f':put_litter_in_its_place: Message sent by {payload.cached_message.author.mention} deleted in <#{payload.channel_id}>', color = discord.Colour.dark_red())
          embed.add_field(name=f"Deleted By", value=f"{payload.cached_message.author.mention}")
          embed.add_field(name="Message", value=f"{payload.cached_message.content}")
          embed.set_footer(text="MESSAGE DELETE", icon_url=self.bot.user.avatar)
          await channel.send(embed=embed)


    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        if before.author.bot:
            return
        data = await self.db.find_one({"guild": before.guild.id})     
        x = data["log-channel"]
        if x == None:
          return
        else: 
          channel = self.bot.get_channel(x)
          embed = discord.Embed(description=f":pencil: Message sent by {before.author.mention} edited in {before.channel.mention} [Jump to message](https://discord.com/channels/{before.guild.id}/{before.channel.id}/{before.id})", color = discord.Colour.gold())
          embed.add_field(name="Before:", value=f"```{before.content}```")
          embed.add_field(name="After:", value=f"```{after.content}```")
          embed.set_author(name=before.author.name, icon_url=before.author.avatar)
          embed.set_footer(text=f"EDITED")
          await channel.send(embed=embed)

    # BAN AND UNBAN

    @commands.Cog.listener()
    async def on_member_ban(self, member):
        with open("./data/databases/logging.json") as f:
            channel_id = json.load(f)
            x = channel_id[str(member.guild.id)]
            channel = self.bot.get_channel(x)
            embed = discord.Embed(description="Member has been banned from this server.", color = discord.Colour.dark_red())
            embed.add_field(name="User", value=f"{member.name}")
            embed.set_author(name=f"{member.name}#{member.discriminator}", icon_url=f"{member.avatar}")
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_unban(self, member):
        with open("./data/databases/logging.json") as f:
            channel_id = json.load(f)
            x = channel_id[str(member.guild.id)]
            channel = self.bot.get_channel(x)
            embed = discord.Embed(description="Member has been unbanned from this server.")
            embed.add_field(name="User", value=f"{member.name}")
            embed.set_author(name=f"{member.name}#{member.discriminator}", icon_url=f"{member.avatar}")
            await channel.send(embed=embed)
        
    # EMOJI CREATE AND EMOJI REMOVE

    @commands.Cog.listener()
    async def on_guild_emoji_create(self, emoji):
        with open("./data/databases/logging.json") as f:
            channel_id = json.load(f)
            x = channel_id[str(emoji.guild.id)]
            channel = self.bot.get_channel(x)
            embed = discord.Embed(description=f"Emoji ({emoji}) has been added.", color = DEFAULT_COLOR)
            embed.set_footer(text="EMOJI CREATE", icon_url=f"{self.bot.user.avatar}")
            await channel.send(embd=embed)

    @commands.Cog.listener()
    async def on_guild_emoji_remove(self, emoji):
        with open("./data/databases/logging.json") as f:
            channel_id = json.load(f)
            x = channel_id[str(emoji.guild.id)]
            channel = self.bot.get_channel(x)
            embed = discord.Embed(description=f"Emoji ({emoji}) has been deleted.", color = discord.Colour.dark_red())
            embed.set_footer(text="EMOJI DELETE", icon_url=f"{self.bot.user.avatar}")
            await channel.send(embd=embed)

def setup(bot):
    bot.add_cog(logging(bot))