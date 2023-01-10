import discord
import asyncio
from discord.ext import commands

class adminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guild = None
        self.mention = None
        self.reason = None

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        if guild.system_channel is not None:
            to_send = f'Hi, {member.mention}! Welcome to {guild.name}!'
            await guild.system_channel.send(to_send)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.startswith('!editme'):
            msg = await message.channel.send('10')
            await asyncio.sleep(3.0)
            await msg.edit(content='40')
        elif message.content.startswith('!deleteme'):
            msg = await message.channel.send('Delit dis')
            await msg.delete()

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot:
            return
        msg = f'**{before.author}** has edited the message:\n{before.content} -> {after.content}'
        await before.channel.send(msg)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return
        msg = f'**{message.author}** has deleted the message:\n{message.content}'
        await message.channel.send(msg)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("Invalid command. For reference sheet use `k!help`.")
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send(
"""Specified member not found. Check casing if you are using this command w/o mention.
*Note that you can pass only **one** member while using this command.*""")
        elif isinstance(error, commands.MissingRequiredArgument) \
        or isinstance(error, commands.CommandInvokeError) \
        or isinstance(error, commands.BadArgument):
            await ctx.send('Passed incorrect argument(s). For reference sheet use `k!help`.')
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You lack permissions for this command.")

    @commands.command()
    async def user(self, ctx, *, user: discord.Member = None):
        if user is None:
            user = ctx.author
        date_format = "%a, %d %b %Y %I:%M %p"
        embed = discord.Embed(color=discord.Color.purple(), description=user.mention)
        embed.set_author(name=str(user))
        embed.add_field(name="Joined", value=user.joined_at.strftime(date_format))
        members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
        embed.add_field(name="Join position", value=str(members.index(user) + 1))
        embed.add_field(name="Registered", value=user.created_at.strftime(date_format))
        if len(user.roles) > 1:
            role_string = ' '.join([r.mention for r in user.roles][1:])
            embed.add_field(name="Roles ({})".format(len(user.roles) - 1), value=role_string, inline=False)
        perm_string = ', '.join([str(p[0]).replace("_", " ").title() for p in user.guild_permissions if p[1]])
        embed.add_field(name="Guild permissions", value=perm_string, inline=False)
        embed.set_footer(text='ID: ' + str(user.id))
        return await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        if member.guild_permissions.administrator:
            await ctx.channel.send(f'**{member.name}** is Server Administrator.')
        else:
            if reason is None:
                await member.send(
                    f'You have been banned from **{ctx.channel.guild.name}**.\nReason: **Not Specified**')
                await ctx.channel.send(
                    f'**{member.name}** has been banned from this server.\nReason: **Not Specified**')
                await member.ban()
            else:
                await member.send(
                    f'You have been banned from **{ctx.channel.guild.name}**.\nReason: **{reason}**')
                await ctx.channel.send(
                    f'**{member.name}** has been banned from this server.\nReason: **{reason}**')
                await member.ban()

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        if member.guild_permissions.administrator:
            await ctx.channel.send(f'**{member.name}** is Server Administrator.')
        else:
            if reason is None:
                await member.send(
                    f'You have been kicked from **{ctx.channel.guild.name}**.\nReason: **Not Specified**')
                await ctx.channel.send(
                    f'**{member.name}** has been kicked from this server.\nReason: **Not Specified**')
                await member.kick()
            else:
                await member.send(
                    f'You have been kicked from **{ctx.channel.guild.name}**.\nReason: **{reason}**')
                await ctx.channel.send(
                    f'**{member.name}** has been kicked from this server.\nReason: **{reason}**')
                await member.kick()

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=int(0)):
        if amount <= int(2):
            await ctx.channel.send('Specify correct amount of messages (3-100).')
            return
        if amount > int(100):
            await ctx.channel.send('Maximum allowed amount for this command is 100.')
            return
        else:
            await ctx.channel.purge(limit=amount)
            await ctx.channel.send(f'{amount} messages were successfully cleared.')