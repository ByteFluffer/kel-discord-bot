from asyncio.log import logger
import disnake
from disnake.ext import commands, tasks
import mysql.connector
from env import secure
from database import *

intents = disnake.Intents.all()
bot = commands.Bot(intents=intents)


# DISNAKE
@bot.event
async def on_ready():
    await bot.change_presence(activity=disnake.Activity(type=disnake.ActivityType.listening , name="you"))
    print("The bot is ready now!")
    minute.start()


# Keep SQL active
@tasks.loop(seconds=60)
async def minute():
    try:
        Database.cursor.execute("SELECT * FROM Users")
        users = Database.cursor.fetchall()
    except Exception as error:
        pass


# Loading different cogs
bot.load_extension("cogs.community_events")  
bot.load_extension("cogs.leveling")  
bot.load_extension("cogs.roleassignment")  
bot.load_extension("cogs.community_commands")  


# Run bot with token imported from secrets.py
if __name__ == "__main__":
    bot.run(secure.BOT_TOKEN)




