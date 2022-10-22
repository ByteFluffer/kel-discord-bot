from dotenv import load_dotenv
import disnake
from disnake.ext import commands
import mysql.connector
import os

intents = disnake.Intents.all()
bot = commands.Bot(intents=intents)

# TODO: make comments

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

@bot.slash_command(description="Level leader board!")
@commands.cooldown(1, 3, commands.BucketType.user)
async def levelbord(inter):
    # Getting info from DATABASE
    cursor.execute("SELECT * FROM Users")
    result_all = cursor.fetchall()



    embed=disnake.Embed(title="Tile", description="Desc", color=0x00ff00)

    for user_id_from_db in result_all:

        user_id_from_db = result_all[0]
        member_name = (await bot.get_or_fetch_user(user_id_from_db))           
        msg_count_from_db = result_all[1]
    
        embed.add_field(name=member_name, value=msg_count_from_db, inline=False)

    await inter.response.send_message(embed)  



# Message counting
@bot.event
async def on_message(inter):
    if inter.content.lower().startswith("#$@$"):
        print("")

    cursor.execute("SELECT user_id FROM Users")
    result_all = cursor.fetchall()

    if result_all == []:
        cursor.execute(f"INSERT INTO Users (user_id, total_message_count) VALUES ({inter.author.id}, 1)")
        db.commit()
        
    cursor.execute(f"SELECT total_message_count FROM Users WHERE user_id = {inter.author.id}")
    result_all = cursor.fetchone()[0]

    counting_new_total = int(result_all) + 1 

    cursor.execute(f"UPDATE Users SET total_message_count = {counting_new_total} WHERE user_id = {inter.author.id}")
    db.commit()
    print(f"User {inter.author.id} heeft een bericht gestuurd op de server!")


bot.run(os.getenv("bot_token"))