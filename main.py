from asyncio.log import logger
import disnake
from disnake.ext import commands, tasks
import mysql.connector
from env import *
import cogs.logger as logger
from disnake.ext.commands import Bot
from threading import Thread
from flask import Flask, request, json, render_template
from modules.webhooks import *
from database import *
from datetime import datetime
import threading 
import time

# Make flask instance
app = Flask(__name__)

intents = disnake.Intents.all()
bot = commands.Bot(intents=intents)


# DISNAKE
# Getting things ready and making the database connection
@bot.event
async def on_ready():
    await bot.change_presence(activity=disnake.Activity(type=disnake.ActivityType.listening , name="/kel"))
    print("The bot is ready now!")

# Message 
@bot.event
async def on_message(inter):
    
    # Bots to exclude from counting
    if inter.author == bot.user or inter.author.bot:
        return
    else:
        Database.cursor.execute(f"INSERT INTO analytics (msg_author, msg_time, msg_channel, msg_lenght, msg_word_count) VALUES ('{inter.author.id}', '{datetime.now()}' , '{inter.channel.id}', '{len(inter.content)}', '{len(str(inter.content).split())}')")
        Database.db.commit()    

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


# Loading different cogs
bot.load_extension("cogs.logger") 
bot.load_extension("cogs.community")  
bot.load_extension("cogs.admin_functions")  
bot.load_extension("cogs.on_member")  
bot.load_extension("cogs.analytics")  



# Making flask rub
def flask_run_instance():
    app.run('0.0.0.0', 5000, debug=False)


# Keeping SQL connection alive!
def thread_one():
    print("Done")
    Database.cursor.execute("SELECT * FROM analytics")
    time.sleep(55)

# Run bot with token imported from secrets.py and running flask
if __name__ == "__main__":
    bot.run(secure.BOT_TOKEN)
    thread_2 = threading.Thread(target=thread_one)
    thread_2.start()        

