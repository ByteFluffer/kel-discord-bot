from dotenv import load_dotenv
import disnake
from disnake.ext import commands
import mysql.connector
import os

intents = disnake.Intents.all()
bot = commands.Bot(intents=intents)

load_dotenv()

@bot.event
async def on_ready():
    await bot.change_presence(activity=disnake.Activity(type=disnake.ActivityType.listening , name="/kel"))
    global cursor
    global db
    db = mysql.connector.connect(
    host=os.getenv("database_ipadress"),
    user= os.getenv("database_username"),
    password=os.getenv("database_password"),
    database=os.getenv("database_name"),
    auth_plugin="mysql_native_password"
    )
    cursor = db.cursor(buffered=True)
    print("The bot is ready!")

# Welcome a new member
@bot.event
async def on_member_join(member):
    print(f"{member} is erbij gekomen!")
    channel = bot.get_channel(1002208150545510402)
    await channel.send(f"Welkom {member.mention} op mijn server! Bij vragen of support ping gerust de admin rol! :heart:")

# Saying goodby to a member
@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(1002208150545510402)
    await channel.send(f"{member.name} is helaas vertrokken!")

# Testing online status of the bot
@bot.slash_command(description="Test of ik nog werk!")
@commands.cooldown(1, 3, commands.BucketType.user)
async def ping(inter):
    await inter.response.send_message(f"Pong! De latency van mij is: {round(bot.latency, 1)}ms.")  
      
@bot.event
async def on_message(inter):
    if inter.content.lower().startswith("#$@$"):
        print("")

    cursor.execute("SELECT user_id FROM Users")
    result_all = cursor.fetchall()

    if result_all == []:
        cursor.execute(f"INSERT INTO Users (user_id, total_message_count) VALUES ({inter.author.id}, 1)")
        db.commit()
    else:
        cursor.execute(f"SELECT total_message_count FROM Users WHERE user_id = {inter.author.id}")
        result_all = cursor.fetchall()
        print(result_all)
        print("Wel een user")




bot.run(os.getenv("bot_token"))