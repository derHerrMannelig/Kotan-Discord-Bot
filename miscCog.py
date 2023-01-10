import discord
import aiohttp
import random
import os
from discord.ext import commands

class miscCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.responses = ["Oh yes, most certainly.",
                          "No way.",
                          "It doesn't matter.",
                          "Chill, dude.",
                          "Daring today, aren't we?",
                          "Yes, but it isn't worth it.",
                          "Never ever!",
                          "Chances are 100%!",
                          "1/100 probability.",
                          "Try again, my vision is foggy."]
        self.emotes = ["<:crying:1011232439676448768>",
                       "<:grr:1011232552465477653>",
                       "<:melm:1011232198663344169>",
                       "<:misery:1011232205525233725>",
                       "<:pog:1011232437923233854>",
                       "<:sad:1011232555128848384>",
                       "<:silly:1011232199896481815>",
                       "<:staring:1011232204153688074>",
                       "<a:comfort:1011232201871998997>",
                       "<a:laugh:1011232436920791040>",
                       "<a:pop:1011232443807826020>"]

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        content = message.content
        if "kotan" in content.lower() or "<@1003175269693136916>" in content:
            await message.add_reaction(random.choice(self.emotes))

    @commands.command()
    async def say(self, ctx, *, post=None):
        if post is None:
            await ctx.channel.send('Specify message.')
        else:
            await ctx.send(post)

    @commands.command()
    async def avatar(self, ctx, *,  member: discord.Member=None):
        if member is None:
            member = ctx.author
        embed = discord.Embed(title=str(member), color=discord.Color.purple())
        embed.set_image(url=member.avatar.url)
        await ctx.send(embed=embed)

    @commands.command()
    async def bonk(self, ctx, *, member: discord.Member = None):
        if member is None:
            await ctx.send('Specify member.')
        else:
            await ctx.send(f"{member.mention}, get bonk'd lol!", file=discord.File('bonk/' + random.choice(os.listdir('bonk'))))

    @commands.command()
    async def question(self, ctx, *, question=None):
        responses = self.responses
        if question is None:
            await ctx.channel.send('Specify question.')
        else:
            await ctx.send(f'My answer is: **{random.choice(responses)}**')

    @commands.command()
    async def roll(self, ctx, dice: str):
        rolls, limit = map(int, dice.split('d'))
        if limit > 20 or rolls > 20:
            await ctx.channel.send('This command is limited by the value of 20.')
        else:
            result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
            await ctx.send(result)

    @commands.command()
    async def cat(self, ctx):
        async with aiohttp.ClientSession() as session:
            imgrequest = await session.get('https://some-random-api.ml/img/cat')
            imgjson = await imgrequest.json()
            factrequest = await session.get('https://some-random-api.ml/facts/cat')
            factjson = await factrequest.json()
        embed = discord.Embed(title="Here is your kitty, kind stranger!", color=discord.Color.purple())
        embed.set_image(url=imgjson['link'])
        embed.set_footer(text=factjson['fact'])
        await ctx.send(embed=embed)