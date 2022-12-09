from asyncio.log import logger
import disnake
from disnake.ext import commands, tasks
import mysql.connector
from secrets import secure
import cogs.logger as logger
from disnake.ext.commands import Bot
from threading import Thread
from flask import Flask, request, json, render_template
from modules.webhooks import *
import env_variable as env_var
# Make flask instance
app = Flask(__name__)

intents = disnake.Intents.all()
bot = commands.Bot(intents=intents)

# TODO: Add comments to admin_functions.py & logger.py test

# DISNAKE
# Getting things ready and making the database connection
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
      

# FLASK
# default making route and checking method
@app.route('/default', methods=["GET"])
def default():
    # Printing IP visitor
    print(f"IP: {request.remote_addr}, user: {request.remote_user}")

    return render_template("index.html")


# UPTIME making route and checking method
@app.route('/uptime', methods=["POST"])
def uptime():
    # Printing IP visitor
    print(f"IP: {request.remote_addr}, user: {request.remote_user}")

    # Call uptime_embed in handling.py with info
    embed = webhook_uptime_handling(request.json)
    send_to_channel(embed, channel=1034947233168236585)

    # Returns OK
    return "Ok"   


# GITHUB making route and checking method
@app.route('/githubIssue', methods=["POST"])
def github():
    # Printing IP visitor
    print(f"IP: {request.remote_addr}, user: {request.remote_user}")

    # If a issue is made on repo, call webhook_print()
    
    if request.json["issue"] != KeyError:
        embed = webhook_github_handling("issue", request.json)
        send_to_channel(embed, channel=1031839675381469204)

    # If a pull request is made on repo, call webhook_print()
    elif request.json["pull"] != KeyError:
        embed = webhook_github_handling("pull", request.json)
        send_to_channel(embed, channel=1031839675381469204)

    # If a pull request is made on repo, call webhook_print()
    elif request.json["push"] != KeyError:
        embed = webhook_github_handling("push", request.json)
        send_to_channel(embed, channel=1031839675381469204)

    # Returns OK
    return "Ok"   


# Server logins making route
@app.route('/server-logins', methods=["POST"])
def uptime():
    # Printing IP visitor
    print(f"IP: {request.remote_addr}, user: {request.remote_user}")

    # Call uptime_embed in handling.py with info
    webhook_server_login_handling(request.json)
    #send_to_channel(embed, channel=1034947233168236585)

    # Returns OK
    return "Ok"   



# Sending to a channel inside GUILD
def send_to_channel(embed, channel):
    channel_def = bot.get_channel(int(channel))
    bot.loop.create_task(channel_def.send(embed=embed))



# DISNAKE
# Message counting
@bot.event
async def on_message(inter):
    
    # Bots to exclude from counting
    bot_list_id = [979415217337401424, 979415217337401424, 1033722440158814288, 1007766943585026141]
    if inter.author.id not in bot_list_id:
        
        # Getting users from db:
        cursor.execute(f"SELECT * FROM Users WHERE user_id = {inter.author.id}")
        result_user = cursor.fetchall()
        
        # If result is empty list, do a insert into the database
        if result_user == []:
            cursor.execute(f"INSERT INTO Users (user_id, total_message_count) VALUES ({inter.author.id}, 1)")
            db.commit()
            
        # If user is in the database, do a select to database
        cursor.execute(f"SELECT total_message_count FROM Users WHERE user_id = {inter.author.id}")
        result_user = cursor.fetchone()[0]
        
        # Adding + 1 from database total_message_count, and update the database with new value
        counting_new_total = int(result_user) + 1
        
        cursor.execute(f"UPDATE Users SET total_message_count = {counting_new_total} WHERE user_id = {inter.author.id}")
        db.commit()
        

        
# Check if user hase more then 5 messageg, if yes print them (going to change)
@tasks.loop(seconds=60)
async def minute():
    cursor.execute("SELECT * FROM Users")
    users = cursor.fetchall()
    for user in users:
        if user[1] > 5:
            member = user[0]
            print(f"User {member} meer dan 5 messages")


# Loading different cogs
bot.load_extension("cogs.logger") 
bot.load_extension("cogs.community")  
bot.load_extension("cogs.admin_functions")  
bot.load_extension("cogs.on_member")  



def flask_run_instance():
    app.run('0.0.0.0', 5000, debug=False)

Thread(target=flask_run_instance).start()

# Run bot with token imported from secrets.py and running flask
if __name__ == "__main__":
    bot.run(secure.bot_token)

