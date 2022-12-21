from types import NoneType
import disnake
from disnake.ext import commands
from disnake import TextInputStyle
from database import *
import mysql.connector
from env import *
import requests

intents = disnake.Intents.all()
bot = commands.Bot(intents=intents)

# EMBED colors
EMBED_DANGER = 0xFF0000
EMBED_GOOD = 0x00FF00
EMBED_ORANGE = 0xFFA500

global guild    


# Cogs class
class Community(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
        # Welcome a new member
        @bot.event
        async def on_member_join(member):
            print(f"{member} is erbij gekomen!")
            
            # Sending something to general channel
            channel = bot.get_channel(1002208150545510402)
            await channel.send(f"Welkom {member.mention} op mijn server! Bij vragen of support ping gerust de admin rol! :heart:")
            
            # Adds user role: "Nieuwe user"
            role = member.guild.get_role(1033382789543903244)
            await member.add_roles(role)


        # Saying goodby to a member
        @bot.event
        async def on_member_remove(member):
            
            # Sending goodbye message in general
            channel = bot.get_channel(1002208150545510402)
            await channel.send(f"{member.mention} is helaas vertrokken!")
            
            # Auto clear database
            userIDs_in_server = []
            
            # Getting all Guild members
            guild = await bot.fetch_guild(1002208148930691172)
            members = await guild.fetch_members(limit=2000).flatten()
            
            # Adds User ID's to list
            for member in members:
                userIDs_in_server.append(member.id)
            
            # Get all users from DB
            Database.cursor.execute("SELECT * FROM Users")
            dbUsers = Database.cursor.fetchall()
            
            # Checks if user is in guild and database by userID
            for dbuser in dbUsers:
                if dbuser[0] in userIDs_in_server:
                    print(f"User {dbuser[0]} still lives in the guild!")
                    
                # If user is isn't in guild, but in database, delete user
                Database.ursor.execute("DELETE FROM Users WHERE user_id = " + str(dbuser[0]))
                Database.db.commit()
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
            
            # Get Channel ID where / command was send in
            get_channel_id = inter.channel.id         
            
            # Sending a embed with "Solved" in it. Also show who executed the command
            embed=disnake.Embed(title="Opgelost!", description=f"Ik heb deze thread als opgelost gemarkeerd! Thread is gesloten door {inter.author.mention}", color=EMBED_GOOD)
            await inter.response.send_message(embed=embed)  
            
            # Define thread, give it the forum channel id
            thread = bot.get_channel(get_channel_id)
            
            # Adds tag to the Forum thread
            tags = thread.parent.get_tag_by_name("Solved")
            await thread.add_tags(tags)
            
            # Archives the given thread
            await thread.edit(archived=True)            


        # Poll function
        @bot.slash_command(description="Maak een poll aan!")
        @commands.cooldown(1, 3, commands.BucketType.user)
        async def poll_create(inter, question: str, choice_1 = None, choice_2 = None, choice_3 = None, choice_4 = None):
            
            # First part embed
            embed=disnake.Embed(title="POLL", description=f"Question: {question}", color=EMBED_GOOD)
            
            # Adding embed field if given choice is filled in, else do nothing. Line 119-129
            if choice_1 != None:
                embed.add_field(name=choice_1, value=":one:", inline=False)
                
            if choice_2 != None:
                embed.add_field(name=choice_2, value=":two:", inline=False)
                
            if choice_3 != None:
                embed.add_field(name=choice_3, value=":three:", inline=False)
                
            if choice_4 != None:
                embed.add_field(name=choice_4, value=":four:", inline=False)
                                              
            # Gets poll creator user avatar
            user_avatar = (await bot.get_or_fetch_user(inter.author.id)).avatar

            # Adds user avatar to embed
            embed.set_footer(text = f"Aangemaakt door {inter.author.name}", icon_url = user_avatar)
            
            # Sending the embed to the channel
            await inter.response.send_message(embed=embed) 
            
            # If choice_1 was filled in, add a reaction to the embed. Etc etc line: 141-155
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

            
        # Python code execute function
        @bot.slash_command(description="Run some Python code")
        async def python_run(inter, code=None):
            
            if code != None:
                request = requests.post("http://93.119.15.103:8060/eval", json={"input": code}).json()
                returncode = request["returncode"]
                code_response = request["stdout"]
                
                await inter.response.send_message(f"""
                                            Your code request job has completed with code {returncode}.
                                            ```py
                                            {code_response}
                                            ```
                                            """)

            # Subclassing the modal.
            class MyModal(disnake.ui.Modal):
                def __init__(self):
                    # The details of the modal, and its components
                    components = [

                        disnake.ui.TextInput(
                            label="COde:",
                            placeholder="Voorbeeld: print('Hello world')",
                            custom_id="description",
                            style=TextInputStyle.paragraph,
                        ),
                    ]
                    super().__init__(
                        title="Vul Python code in",
                        custom_id="create_tag",
                        components=components,
                    )

                # The callback received when the user input is completed.
                async def callback(self, inter: disnake.ModalInteraction):

                    
                    for value in inter.text_values.items():
                        request = requests.post("http://93.119.15.103:8060/eval", json={"input": value[1]}).json()
                        returncode = request["returncode"]
                        code_response = request["stdout"]                        
                        
                        await inter.response.send_message(f"""
                            Your code request job has completed with code {returncode}.
                            
                            ```py
\n                            
{code_response}```""")
                            
                            
                            
                            
                                     
                        

            await inter.response.send_modal(modal=MyModal())

# Adds it to the main
def setup(bot: commands.Bot):
    bot.add_cog(Community(bot))
    
    
    


    