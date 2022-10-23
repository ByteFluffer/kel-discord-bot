import disnake
from disnake.ext import commands
import time
import mysql.connector
from secrets import secure

# EMBED colors:
EMBED_DANGER = 0xFF0000
EMBED_GOOD = 0x00FF00
EMBED_ORANGE = 0xFFA500

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

class AdminFunctions(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
        # Admin management commands
        @bot.slash_command(description="Verwijder meerdere berichten tegelijk! (admin only!)")
        async def purge_admin(inter, berichten_aantal: int):
            if not inter.author.guild_permissions.administrator:
                await inter.response.send_message("Sorry, deze functie is niet toegankelijk voor non-admins!")
            channel = inter.channel    
            await channel.purge(limit=berichten_aantal)
            await inter.response.send_message(f"Ik heb {berichten_aantal} berichten verwijderd!", delete_after=4.0)  

        # Admin community commands
        @bot.slash_command(description="Maak een announcement! (admin only!)")
        async def announce_admin(inter, kanaal: disnake.TextChannel, announcement: str):
            if not inter.author.guild_permissions.administrator:
                await inter.response.send_message("Sorry, deze functie is niet toegankelijk voor non-admins!")
            
            embed=disnake.Embed(title="Announcement!", description=f"Door: {inter.author.mention}", color=EMBED_GOOD)
            embed.add_field(name="Announcement:", value=announcement, inline=False)
            Announce_channel = bot.get_channel(kanaal.id)
            await Announce_channel.send(embed=embed) 
            await inter.response.send_message(f"Ik heb {announcement} naar: {kanaal} gestuurd!", delete_after=4.0)  


        # Admin community commands
        @bot.slash_command(description="Schoon de database op! (admin only!)")
        async def database_clear_admin(inter):
            if not inter.author.guild_permissions.administrator:
                await inter.response.send_message("Sorry, deze functie is niet toegankelijk voor non-admins!")
            
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
                else:
                    cursor.execute("DELETE FROM Users WHERE user_id = " + str(dbuser[0]))
                    db.commit()
                    print(f"I deleted user: {dbuser[0]}, i think he moved out!")

            await inter.response.send_message("I deleted all the not in server members from the database!")  

                    
def setup(bot: commands.Bot):
    bot.add_cog(AdminFunctions(bot))        