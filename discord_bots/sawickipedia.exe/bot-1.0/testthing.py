import discord
from discord.ext import commands

description = "Test"

bot = commands.Bot(command_prefix="???", description=description)

@bot.event  
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)  
    print('------')

@bot.command()
async def testcommandthing(ctx):
    channel = await bot.get_user_info(120195047470661632)
    await channel.send("<:trollface:453272230516752406>")

bot.run("")
