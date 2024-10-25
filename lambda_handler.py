import os
import json
import discord
from discord import app_commands

# Discordクライアントの設定
class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

client = MyClient()

@client.tree.command()
async def start(interaction: discord.Interaction):
    """Simple command that responds with hello"""
    await interaction.response.send_message('hello')

def lambda_handler(event, context):
    """Lambda function handler"""
    try:
        # Discord BOTトークンを環境変数から取得
        TOKEN = os.environ['DISCORD_BOT_TOKEN']

        # イベントデータの解析
        body = json.loads(event['body'])

        # Pingイベントの処理
        if body['type'] == 1:
            return {
                'statusCode': 200,
                'body': json.dumps({'type': 1})
            }

        # コマンドの処理
        client.run(TOKEN)

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Command processed successfully'})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }