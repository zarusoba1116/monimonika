import discord
from discord.ext import commands
from os import getenv
import random

TOKEN = getenv('DISCORD_BOT_TOKEN')
intents = discord.Intents.all()
intents.typing = False
bot = commands.Bot(command_prefix='$',help_command=None,case_insensitive=True,intents=intents)

@bot.listen("on_message")
async def on_message(message):
    if message.author.bot:
        return

@bot.command(name='dice')
async def dice(ctx):
    dice = random.randint(1, 6)
    await ctx.send(f"今回の出目は**{dice}**です")

@bot.command(name='guild')
async def guild(ctx):
    guild = ctx.guild.name
    await ctx.send(f"サーバー名は**{guild}**です")

@bot.command(name='servericon')
async def get_server_icon(ctx):
    # コマンドが実行されたサーバーのアイコンURLを取得
    icon_url = ctx.guild.icon_url
    
    # サーバーのアイコンURLが存在する場合
    if icon_url:
        # アイコンを送信者にDMで送信
        await ctx.author.send(f"サーバーのアイコン: {icon_url}")
    else:
        # アイコンが存在しない場合はエラーメッセージを送信
        await ctx.send("サーバーのアイコンが見つかりませんでした。")


bot.run(TOKEN)
