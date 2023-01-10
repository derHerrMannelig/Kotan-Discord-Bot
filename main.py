import os
import discord
from discord.ext import commands
from miscCog import miscCog
from adminCog import adminCog
# from musicCog import musicCog
from keepAlive import keep_alive

intents = discord.Intents.all() # Bot requires full Administrator privileges.
bot = commands.Bot(command_prefix=['k!', 'K!'], case_insensitive=True, intents=intents)
bot.remove_command('help')
# NOTE — if you want to host this bot locally — cut and paste add_cogs here w/o await statement.

@bot.event
async def on_ready():
    print(f'{bot.user} is online!')
    await bot.change_presence(activity=discord.Game('k!help'))
    await bot.add_cog(miscCog(bot))
    await bot.add_cog(adminCog(bot))
  # await bot.add_cog(musicCog(bot))

@bot.command()
async def help(ctx):
    await ctx.send(
"""**List of commands:**
`k!cat` — posts random cat image and quote (powered by Some Random Api).
`k!roll XdY` — rolls a dice, `X` - number of dice, `Y` - number of sides (max X & Y 20).
`k!question *question*` — posts random answer.
`k!user @user` — displays info about mentioned guild member (w/o mention displays your member info).
`k!avatar @user` — extracts profile picture of the specified member.
`k!say *message*` — repeats your text message.
`k!bonk @user` — bomks umser. Yemp.
**List of moderation commands (specific permissions required):**
`k!kick @user *reason*` — kicks user and sends kick reason in DM.
`k!ban @user *reason*` — bans user and sends ban reason in DM.
`k!clear *amount*` — clears specific amount of messages (range 3-100).
**List of features:**
This bot greets newcomers.
This bot indicates edited messages and displays changes.
This bot indicates deleted messages and posts them.
*Try mentioning Kotan in your discussion — and it will react!*"""
    )

keep_alive()
secret = os.environ['TOKEN']
# NOTE - setup secret variable according to your development environment settings.
bot.run(secret)
