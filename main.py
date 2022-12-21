from asyncio.log import logger
import disnake
from disnake.ext import commands, tasks
import mysql.connector
from env import secure
from disnake.ext.commands import Bot
from threading import Thread
from flask import Flask, request, json, render_template
from modules.webhooks import *
from database import *


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
    print("The bot is ready now!")
      

@bot.event
async def on_message(inter):
    pass      



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
def serverlogins():
    # Printing IP visitor
    print(f"IP: {request.remote_addr}, user: {request.remote_user}")

    # Call uptime_embed in handling.py with info
    embed = webhook_server_login_handling(request.json)
    send_to_channel(embed, channel=1050823395169804358)

    # Returns OK
    return "Ok"   



# Sending to a channel inside GUILD
def send_to_channel(embed, channel):
    channel_def = bot.get_channel(int(channel))
    bot.loop.create_task(channel_def.send(embed=embed))


        
# Keep SQL active
@tasks.loop(seconds=60)
async def minute():
    Database.cursor.execute("SELECT * FROM Users")
    users = Database.cursor.fetchall()



# Loading different cogs
bot.load_extension("cogs.on_member")  



def flask_run_instance():
    app.run('0.0.0.0', 5000, debug=False)

Thread(target=flask_run_instance).start()


# Run bot with token imported from secrets.py and running flask
if __name__ == "__main__":
    bot.run(secure.BOT_TOKEN)

