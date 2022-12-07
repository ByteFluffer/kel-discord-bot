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
      


# default making route and checking method
@app.route('/', methods=["GET"])
async def default():
    return render_template("index.html")


# UPTIME making route and checking method
@app.route('/uptime', methods=["GET", "POST"])
async def uptime():
    # If method is GET, return error page
    if request.method != "POST":
      return render_template("error_invalid_method.html")

    # Call uptime_embed in handling.py with info
    embed = webhook_uptime_handling(request.json)

    channel = bot.get_channel(env_var.UPTIME_CHANNEL_ID)
    print(channel)
    bot.loop.create_task(channel.send(embed=embed))
    print("Jeej")

    # Returns data
    return request.json







# GITHUB making route and checking method
@app.route('/githubIssue', methods=["GET", "POST"])
async def github():
    # If method is GET, return error page
    if request.method != "POST":
      return render_template("error_invalid_method.html")

    # If a issue is made on repo, call webhook_print()
    if request.json["issue"] != KeyError:
        webhook_github_handling("issue", request.json)
        pass
    # If a pull request is made on repo, call webhook_print()
    elif request.json["pull"] != KeyError:
        print(request.json["repository"]["name"])
        webhook_github_handling("pull", request.json)
        pass

    # Returns data
    return request.json      



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

