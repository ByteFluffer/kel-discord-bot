from asyncio.log import logger
import disnake
from disnake.ext import commands
import mysql.connector
import os
from secrets import secure

import cogs.logger as logger
from disnake.ext.commands import Bot

import threading
from threading import Timer

intents = disnake.Intents.all()
bot = commands.Bot(intents=intents)


# Getting things ready
@bot.event
async def on_ready():
    await bot.change_presence(activity=disnake.Activity(type=disnake.ActivityType.listening , name="/kel"))
    global cursor
    global db
    db = mysql.connector.connect(
    host= secure.database_ipadress,
    user= secure.database_username,
    password= secure.database_password,
    database= secure.database_name,
    auth_plugin="mysql_native_password"
    )
    cursor = db.cursor(buffered=True)
    print("The bot is ready now!")
    await minute()


# Message counting
@bot.event
async def on_message(inter):
  
    if inter.author.id not in bot_list_id:
        # Getting users from db:
        cursor.execute(f"SELECT * FROM Users WHERE user_id = {inter.author.id}")
        result_user = cursor.fetchall()
        
        if result_user == []:
            cursor.execute(f"INSERT INTO Users (user_id, total_message_count) VALUES ({inter.author.id}, 1)")
            db.commit()
            
        # If user is in the database
        cursor.execute(f"SELECT total_message_count FROM Users WHERE user_id = {inter.author.id}")
        result_user = cursor.fetchone()[0]
        
        counting_new_total = int(result_user) + 1
        cursor.execute(f"UPDATE Users SET total_message_count = {counting_new_total} WHERE user_id = {inter.author.id}")
        db.commit()
        
        

# Level leader board
@bot.slash_command(description="Level leader board!")
async def levelbord(inter):
    
    # Getting info from DATABASE
    cursor.execute("SELECT * FROM Users ORDER BY total_message_count DESC")
    result_all = cursor.fetchall()

    embed=disnake.Embed(title="Level bord!", description="Van hoog naar laag:", color=0x00ff00)

    for user_from_db in result_all:
        user_id_from_db = user_from_db[0]
        msg_count_from_db = user_from_db[1]
        name_user = (await bot.get_or_fetch_user(user_id_from_db)).name             
        embed.add_field(name=f"Gebruiker: {name_user}", value=f"Totaal aantal berichten: {msg_count_from_db}", inline=False)
    
    embed.set_footer(text="By </Kelvin>", icon_url="https://itkelvin.nl/CustomCPULOGO.png")
    await inter.response.send_message(embed=embed)  
    
async def minute():
    threading.Timer(60, minute).start()
    cursor.execute("SELECT * FROM Users")
    users = cursor.fetchall()
    for user in users:
        if user[1] > 5:
            member = user[0]
            print(f"User {member} meer dan 5 messages")
    
# Loading different modules
bot.load_extension("cogs.logger") 
bot.load_extension("cogs.community")  
bot.load_extension("cogs.admin_functions")  
    
bot.run(secure.bot_token)

