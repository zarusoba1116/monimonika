import discord
from discord.ext import commands
from os import getenv
import random

TOKEN = getenv('DISCORD_BOT_TOKEN')

intents = discord.Intents.all()
intents.typing = False
bot = commands.Bot(command_prefix='$', intents=intents)

# ゲームの設定
INITIAL_FUND = 1000

class ChinchirorinCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.players = {}  # 参加者とその資金の辞書

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.bot.user} がログインしました')

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if message.content.startswith('!start'):
            await self.start_game(message)
        elif message.content.startswith('!join'):
            await self.join_game(message)
        elif message.content.startswith('!play'):
            await self.play_round(message)

    async def start_game(self, message):
        if len(self.players) == 0:
            self.players[message.author.id] = INITIAL_FUND  # 最初の親の資金を設定
            await message.channel.send(f'{message.author.mention} がゲームを開始しました。')
            await message.channel.send('参加者は`!join`コマンドで参加してください。')
        else:
            await message.channel.send('ゲームが既に進行中です。')

    async def join_game(self, message):
        if message.author.id not in self.players:
            self.players[message.author.id] = INITIAL_FUND  # 参加者の初期資金を設定
            await message.channel.send(f'{message.author.mention} がゲームに参加しました。')
        else:
            await message.channel.send(f'{message.author.mention} は既にゲームに参加しています。')

    async def play_round(self, message):
        if len(self.players) < 2:
            await message.channel.send('参加者が足りません。')
            return

        # 親の選択
        parent_id = max(self.players, key=self.players.get)
        parent_fund = self.players[parent_id]

        # ゲーム開始メッセージ
        start_message = f'ゲームを開始します。親は {message.guild.get_member(parent_id).mention} です。'
        await message.channel.send(start_message)

        # ゲーム実行
        for player_id, fund in self.players.items():
            if player_id != parent_id:
                player = message.guild.get_member(player_id)
                await message.channel.send(f'{player.mention} の資金: {fund}')

                # サイコロを振る
                dice_result = random.randint(1, 6)
                await message.channel.send(f'{player.mention} がサイコロを振りました。結果: {dice_result}')

                # ゲーム結果の判定と処理
                if dice_result == 6:
                    await message.channel.send('親の勝ちです！コマの総取りです。')
                    parent_fund += fund
                    self.players[player_id] = 0
                elif dice_result == 4 or dice_result == 5:
                    await message.channel.send('親の勝ちです！コマの倍額を受け取ります。')
                    parent_fund += fund
                    self.players[player_id] = 0
                elif dice_result == 1 or dice_result == 2 or dice_result == 3:
                    await message.channel.send('親の負けです。コマを支払います。')
                    parent_fund -= fund
                    self.players[player_id] = 0
                await message.channel.send(f'{message.guild.get_member(parent_id).mention} の残り資金: {parent_fund}')

        # 新しい親の選択
        new_parent_id = max(self.players, key=self.players.get)
        if new_parent_id != parent_id:
            await message.channel.send(f'{message.guild.get_member(new_parent_id).mention} が新しい親になりました。')
        else:
            await message.channel.send('ゲーム終了です。')
        self.players = {new_parent_id: parent_fund}  # 新しい親のみ残す

bot.add_cog(ChinchirorinCog(bot))
bot.run(TOKEN)
