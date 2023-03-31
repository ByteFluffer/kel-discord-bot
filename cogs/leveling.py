
import disnake
from disnake.ext import commands, tasks
from env import *
from database import Database


class leveling(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # Starting tasks
        self.scoreboard_loop.start()

    # On message 
    @commands.Cog.listener()
    async def on_message(self, message):
        # If the message isnt from a bot
        if message.author != self.bot.user or message.author.bot:
            # If user id isn't in the list, add it
            if message.author.id not in self.list_users:
                self.list_users.append(message.author.id)
                print(self.list_users)





    list_users = []
    @tasks.loop(seconds=10) 
    async def scoreboard_loop(self):
        XP = 5

        for user in self.list_users:
            if leveling.validate_user(user) != False:
                get_xp = leveling.get_xp(id=user)
                Database.cursor.execute(f"UPDATE scoreboard SET xp = {int(get_xp) + XP} WHERE user_id = {user}")
                Database.db.commit()
                print(f"User {user} gained xp: {int(get_xp) + XP}")

            else:
                Database.cursor.execute(f"INSERT INTO scoreboard (user_id, xp) VALUES ({int(user)}, {XP})")
                Database.db.commit()
                print(f"User {user} gained xp: 7")
        
        # Clearing list
        self.list_users.clear()



                
    # Validate user inside db
    def validate_user(id):
        Database.cursor.execute(f"SELECT * FROM scoreboard WHERE user_id = {id} LIMIT 1")
        res = Database.cursor.fetchone()
        if res == None or res == []:
            return False
        else:
            return True


    # Getting user XP:
    def get_xp(id):
        Database.cursor.execute(f"SELECT xp from scoreboard WHERE user_id = {id} LIMIT 1")
        res = Database.cursor.fetchone()[0]
        return res
    
    
def setup(bot: commands.Bot):
    bot.add_cog(leveling(bot))