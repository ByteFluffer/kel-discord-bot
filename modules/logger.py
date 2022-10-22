import disnake
from disnake.ext import commands

intents = disnake.Intents.all()
bot = commands.Bot(intents=intents)

@bot.event
async def on_guild_channel_delete(channel):
        print(f"Channel deleted: {channel}")

@bot.event
async def on_guild_channel_create(channel):
        print(f"Channel deleted: {channel}")
