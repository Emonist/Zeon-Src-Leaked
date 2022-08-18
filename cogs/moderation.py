import discord
from discord.ext import commands
import aiohttp
from io import BytesIO

class moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tasks = []

    """Moderation commands"""  

    def help_custom(self):
		      emoji = '<a:mod:958707669894594620>'
		      label = "Moderation"
		      description = "Shows all Moderation Commands"
		      return emoji, label, description  

    @commands.command(aliases=['m'])
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx: commands.Context, member: discord.Member, *, reason="No Reason Provided."):
        guild = ctx.guild
        mutedRole = discord.utils.get(guild.roles, name="Muted")

        if not mutedRole:
            mutedRole = await guild.create_role(name="Muted")

            for channel in guild.channels:
                await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)
        if ctx.author.top_role.position > member.top_role.position or ctx.author == guild.owner:
            await ctx.send(f"<a:chr_greentick:958707859649093703> | Successfully muted {member.display_name}")
            await member.add_roles(mutedRole, reason=reason)
            await member.send(f":exclamation: | You have been muted from: {guild.name} reason: {reason}")
        if not ctx.author.top_role.position > member.top_role.position and ctx.author != ctx.guild.owner:
            await ctx.send(f"<:Slansic_error:918015053591085066> | You cannot mute someone with a higher role than you!")

    @commands.command(aliases=['unm'])
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, member: discord.Member):
        mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

        await ctx.send(f"<a:chr_greentick:958707859649093703> | {member.display_name} has been unmuted")
        await member.remove_roles(mutedRole)
        await member.send(f":exclamation: | You are have been unmuted from: {ctx.guild.name}")

    @commands.command(aliases=['purge'])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount = 2):
        if amount > 100:
            await ctx.send('<a:Warn:958738005076619324> | You cannot delete more than 100 messages at once!')
            return
        await ctx.channel.purge(limit = amount)
        await ctx.send(f"<a:chr_greentick:958707859649093703> | {amount} Messages cleared by: {ctx.author.mention}")

    @commands.command(aliases=['k'])
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx: commands.Context, member: discord.Member, *, reason=None):
        if member == self.bot:
            await ctx.send(f"You cannot kick me!")
        if ctx.author.top_role.position > member.top_role.position or member == ctx.guild.owner:
            await member.kick(reason=reason)
            await ctx.send(f"<a:chr_greentick:958707859649093703> | {member.display_name} has been kicked from this guild, for: {reason}")
            await member.send(f":exclamation: | You have been kicked from {ctx.guild.name} for: {reason}!")
        if not ctx.author.top_role.position > member.top_role.position and ctx.author != ctx.guild.owner:
            await ctx.send(f"<a:Warn:958738005076619324> | You cannot kick someone with a higher role than you!")

    @commands.command(name="roleall")
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def role_all(self, ctx, *, role: discord.Role):
        if ctx.guild.id in self.tasks:
            return await ctx.send(embed=discord.Embed(title="Roleall", description="There is a roleall task already running, please wait for it to finish", color=0x01f5b6))
        num = 0
        failed = 0
        for user in list(ctx.guild.members):
            try:
                await user.add_roles(role)
                num += 1
            except Exception:
                failed += 1
        await ctx.send(embed=discord.Embed(title="Roleall", description="Successfully added **`%s`** to **`%s`** users, failed to add it to **`%s`** users" % (role.name, num, failed), color=0x01f5b6))
  
    @commands.command(aliases=['w'])
    @commands.has_permissions(kick_members=True)
    async def warn(self, ctx, member: discord.Member, * , reason="No Reason Provided!"):
        await ctx.send(f"<a:chr_greentick:958707859649093703> | {member.display_name} has been warned for: {reason}")
        await member.send(f":exclamation: | You have been warned in {ctx.guild.name} for: {reason}")


    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def createrole(self, ctx, r=None):
        await ctx.send(f"<a:chr_greentick:958707859649093703> | role {r} has been created successfully.")
        await ctx.guild.create_role(name=r)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def addrole(self, ctx: commands.Context, member: discord.Member, * , role: discord.Role):
        if ctx.author.top_role.position > member.top_role.position:
            await member.add_roles(role)
            await ctx.send(f"<a:chr_greentick:958707859649093703> | {member.display_name} has been given the role {role.name}")
        else:
            await ctx.send('You cannot add a role to someone with a higher role than you!')

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def releterole(self, ctx, rd = discord.Role):
        await ctx.send(f"<a:chr_greentick:958707859649093703> | {rd.name} role has been deleted.")
        await ctx.guild.delete_role(rd)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def removerole(ctx, * , member: discord.Member , rr = discord.Role):
        await ctx.send(f"<a:chr_greentick:958707859649093703> | role {rr.name} has been removed from {member.display_name}")
        await  member.remove_roles(rr)

    @commands.command()
    async def deafen(self, ctx, user: discord.Member, * , reason=None):
        await ctx.send(f"<a:chr_greentick:958707859649093703> | {user.display_name} has been deafened, for: {reason}")
        await user.edit(deafen = True)

    @commands.command()
    async def vcMute(self, ctx, member: discord.Member, * , reason=None):
        await ctx.send(f"<a:chr_greentick:958707859649093703> | {member.display_name} has been muted, for: {reason}")
        await member.edit(mute = True)

    @commands.command()
    async def vcUnmute(self, ctx, member: discord.Member):
        await ctx.send(f"<a:chr_greentick:958707859649093703> | {member.display_name} has been unmuted.")
        await member.edit(mute = False)

    @commands.command()
    async def vcUndeafen(self, ctx, member: discord.Member):
        await ctx.send(f"<a:chr_greentick:958707859649093703> | {member.display_name} has been undeafened.")
        await member.edit(deafen = False)

    @commands.command()
    @commands.has_permissions(manage_emojis=True)
    async def delemoji(self, ctx, emoji: discord.Emoji):
        await emoji.delete()
        await ctx.send(f"<a:chr_greentick:958707859649093703> | emoji has been deleted.")

    @commands.command()
    async def addemoji(self, ctx, url:str, *, name = None):
        if name == None:
            name == "stolen-emoji"
        if url == discord.Emoji:
            url = discord.Emoji.url
        guild = ctx.guild
        async with aiohttp.ClientSession() as ses:
            async with ses.get(url) as r:
                try:
                    imgOrGif = BytesIO(await r.read())
                    bValue = imgOrGif.getvalue()
                    if r.status in range(200, 299):
                        emoji = await guild.create_custom_emoji(image=bValue, name=name)
                        await ctx.send(f"<a:chr_greentick:958707859649093703> | Sucessfully added Emoji `:{name}:`")
                        await ses.close()
                    else:
                        await ctx.send(f"<a:Warn:958738005076619324> | Something went wrong | {r.status}")
                except discord.HTTPException:
                    await ctx.send(f"<a:Warn:958738005076619324> | The file is too big.")


    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx: commands.Context, member: discord.Member, *, reason=None):
        if member == self.bot:
            await ctx.send('You cannot ban the bot!')
        if ctx.author.top_role.position > member.top_role.position or ctx.author == ctx.guild.owner:
            await member.ban(reason=reason)
            await ctx.send(f"<a:chr_greentick:958707859649093703> | {member.display_name} has been successfully banned")
            await member.send(f":exclamation: | You have been banned from {ctx.message.guild.name} for reason: {reason}")
        if not ctx.author.top_role.position > member.top_role.position and ctx.author != ctx.guild.owner:
            await ctx.send(f"<a:Warn:958738005076619324> | You cannot ban someone with a higher role than you.")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, id: int):
        user = await self.bot.fetch_user(id)
        await ctx.guild.unban(user)
        await ctx.send(f"<a:chr_greentick:958707859649093703> | {user.name} has been successfully unbanned")

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def clone(self, ctx, channel: discord.TextChannel):
        await channel.clone()
        await ctx.send(f"<a:chr_greentick:958707859649093703> | {channel.name} has been successfully cloned")

def setup(bot):
    bot.add_cog(moderation(bot))