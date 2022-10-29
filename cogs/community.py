import disnake
from disnake.ext import commands
import mysql.connector
from secrets import secure

intents = disnake.Intents.all()
bot = commands.Bot(intents=intents)
# EMBED colors:
EMBED_DANGER = 0xFF0000
EMBED_GOOD = 0x00FF00
EMBED_ORANGE = 0xFFA500
global cursor
global guild    

db = mysql.connector.connect(
host= secure.database_ipadress,
user= secure.database_username,
password= secure.database_password,
database= secure.database_name,
auth_plugin="mysql_native_password"
)
cursor = db.cursor(buffered=True)


class Community(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
        # Welcome a new member
        @bot.event
        async def on_member_join(member):
            print(f"{member} is erbij gekomen!")
            channel = bot.get_channel(1002208150545510402)
            await channel.send(f"Welkom {member.mention} op mijn server! Bij vragen of support ping gerust de admin rol! :heart:")

            role = member.guild.get_role(1033382789543903244)
            await member.add_roles(role)


        # Saying goodby to a member
        @bot.event
        async def on_member_remove(member):
            channel = bot.get_channel(1002208150545510402)
            await channel.send(f"{member.mention} is helaas vertrokken!")
            
            # Auto clear database
            userIDs_in_server = []
            guild = await bot.fetch_guild(1002208148930691172)
            members = await guild.fetch_members(limit=2000).flatten()
            
            for member in members:
                userIDs_in_server.append(member.id)
            
            cursor.execute("SELECT * FROM Users")
            dbUsers = cursor.fetchall()
            
            for dbuser in dbUsers:
                if dbuser[0] in userIDs_in_server:
                    print(f"User {dbuser[0]} still lives in the guild!")
                    
                # Deleting the user
                cursor.execute("DELETE FROM Users WHERE user_id = " + str(dbuser[0]))
                db.commit()
                print(f"I deleted user: {dbuser[0]}, i think he moved out!")


        # Testing online status of the bot
        @bot.slash_command(description="Test of ik nog werk!")
        @commands.cooldown(1, 3, commands.BucketType.user)
        async def ping(inter):
            await inter.response.send_message(f"Pong! De latency van mij is: {round(bot.latency, 1)}ms.")  


        # Close the forum channel
        @bot.slash_command(description="Markeer dit forum kanaal als opgelost")
        @commands.cooldown(1, 3, commands.BucketType.user)
        async def solved(inter):
            
            get_channel_id = inter.channel.id            
            thread = bot.get_channel(get_channel_id)  # You can also use bot.get_channel(...)
            await thread.edit(archived=True)
            
            embed=disnake.Embed(title="Opgelost!", description=f"Ik heb deze thread als opgelost gemarkeerd! Thread is gesloten door {inter.author.mention}", color=EMBED_GOOD)
            await inter.response.send_message(embed=embed)             
            
            
        # Poll function
        @bot.slash_command(description="Maak een poll aan!")
        @commands.cooldown(1, 3, commands.BucketType.user)
        async def poll_create(inter, question: str, choice_1 = None, choice_2 = None, choice_3 = None, choice_4 = None):
            
            embed=disnake.Embed(title="POLL", description=f"Question: {question}", color=EMBED_GOOD)
            if choice_1 != None:
                embed.add_field(name=choice_1, value=":one:", inline=False)
                
            if choice_2 != None:
                embed.add_field(name=choice_2, value=":two:", inline=False)
                
            if choice_3 != None:
                embed.add_field(name=choice_3, value=":three:", inline=False)
                
            if choice_4 != None:
                embed.add_field(name=choice_4, value=":four:", inline=False)
                                              
            user_avatar = (await bot.get_or_fetch_user(inter.author.id)).avatar

            embed.set_footer(text = f"Aangemaakt door {inter.author.name}", icon_url = user_avatar)
            await inter.response.send_message(embed=embed) 
            
            if choice_1 != None:
                msg = await inter.original_message()
                await msg.add_reaction("1️⃣")

            if choice_2 != None:
                msg = await inter.original_message()
                await msg.add_reaction("2️⃣")

            if choice_3 != None:
                msg = await inter.original_message()
                await msg.add_reaction("3️⃣")

            if choice_4 != None:
                msg = await inter.original_message()
                await msg.add_reaction("4️⃣")


            
        
def setup(bot: commands.Bot):
    bot.add_cog(Community(bot))
    
    
    


    