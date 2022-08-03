import requests
from discord.ext import commands
from musicCog import musicCog

bot = commands.Bot(command_prefix= ['k!','K!'], case_insensitive=True)
bot.remove_command('help')

def get_cat():
  kitty = requests.get('http://thecatapi.com/api/images/get.php')
  if kitty.status_code == 200:
      kitty = kitty.url
      return kitty
  else:
      return 'TheCatApi is down, try again later!'

bot.add_cog(musicCog(bot))

@bot.event
async def on_ready():
    print(f'{bot.user} is online!')
 
@bot.command()
async def help(ctx):
  await ctx.send("List of commands: \
  \n`k!cat` — posts random cat image (powered by TheCatApi)")    

@bot.command()
async def cat(ctx):
  cat = get_cat()
  await ctx.send(cat)

bot.run('TOKEN')
