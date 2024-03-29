import discord
from discord.ext import commands
from os import getenv

TOKEN = getenv('DISCORD_BOT_TOKEN')
intents = discord.Intents.all()
intents.typing = False
bot = commands.Bot(command_prefix='$',help_command=None,case_insensitive=True,intents=intents)

@bot.listen("on_message")
async def on_message(message):
    if message.author.bot:
        return
    else:
        await message.channel.send("Just Monika.")

@bot.command(name='dice')
async def dice(ctx):
    await message.channel.send("Just Monika.")
    

bot.run(TOKEN)
